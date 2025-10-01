from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import schedule
import time
from twitter import tweet_with_image_v2, retweet, reply_with_image_v2, upload_media
from utils import get_days_in_month, remove_file
from message import *
import database
from report_generators import *
from log import init_logger
import logging


def tweet_reports():

    is_hot = True if os.getenv("HOT") == "True" else False

    now = datetime.now()
    one_day = timedelta(days=1)
    tomorrow = now + one_day
    report = generate_day_ahead_report(tomorrow)

    if not report.dataframe.empty:
        # day ahead
        graph_settings = {
            "bar_labels": True,
            "label_rotation": 0,
            "bars_from_start": 5,
            "bar_label_font_size": 8,
        }
        report.plot_bar_graph(graph_settings)
        message_day = compile_day_ahead_message(report, "below_average")
        logging.info("Day-ahead message: \n{}".format(message_day))

        # 7 day
        report_7 = generate_7_day_report(tomorrow)
        graph_settings_7 = {"hourly": True, "label_rotation": 0, "bars_from_start": 32}
        report_7.plot_bar_graph(graph_settings_7)
        message_7 = compile_7_day_message(report_7)
        logging.info("7-day message: {}".format(message_7))

        # 28 day
        report_28 = generate_28_day_report(tomorrow)
        graph_settings_28 = {
            "hourly": False,
            "label_rotation": 45,
            "bars_from_start": 6,
            "bar_label_font_size": 6,
        }
        report_28.plot_bar_graph(graph_settings_28)
        message_28 = compile_28_day_message(report_28)
        logging.info("28-day message: {}".format(message_28))

        # tweet as thread
        if is_hot:

            # tweet day ahead
            media = upload_media([report.bar_graph_path])
            tweet = tweet_with_image_v2(media, message_day)

            # reply to day ahead tweet
            media_7 = upload_media([report_7.bar_graph_path])
            tweet_7 = reply_with_image_v2(
                media_ids=media_7, message=message_7, tweet_id=tweet.data["id"]
            )

            # reply to 7 day tweet
            media_28 = upload_media([report_28.bar_graph_path])
            tweet_28 = reply_with_image_v2(
                media_ids=media_28, message=message_28, tweet_id=tweet_7.data["id"]
            )

            # save first tweet id
            database.add_tweet(report, tweet.data["id"])

            remove_file(report.bar_graph_path)
            remove_file(report_7.bar_graph_path)
            remove_file(report_28.bar_graph_path)

            #shutdown
            os.system('sudo shutdown now')
        else:
            print("The bot is not hot")
    else:
        logging.info("Dataframe is empty, trying again in 10 minutes")
        time.sleep(600)
        tweet_reports()


def tweet_monthly_report(now):

    is_hot = True if os.getenv("HOT") == "True" else False
    one_month = timedelta(days=35)  # to get previous month number

    # current month
    report_current = generate_month_report(now)

    # previous month
    report_previous = generate_month_report(now - one_month)

    graph_settings = {
        "hourly": False,
        "label_rotation": 45,
        "bars_from_start": 6,
        "bar_label_font_size": 6,
    }
    report_current.plot_bar_graph(graph_settings)
    message = compile_monthly_message(report_current, report_previous)
    print(message)

    if is_hot:
        monthly_graph_media = upload_media([report_current.bar_graph_path])
        tweet_with_image_v2(media_ids=monthly_graph_media, message=message)
        remove_file(report_current.bar_graph_path)

    else:
        logging.info("The bot is not hot")


def retweet_day_report():
    now = datetime.now()
    date = f"{str(now.day)}.{str(now.month)}.{str(now.year)}"
    tweet = database.get_tweet(date)
    if tweet:
        id = tweet["tweet_id"]
        retweet(id)
    else:
        logging.info("Tweet id on {} not found from database".format(date))


def check_if_last_day_of_month():
    now = datetime.now()
    is_last_day_of_month = True if now.day == get_days_in_month(now) else False

    if is_last_day_of_month:
        tweet_monthly_report(now)


if __name__ == "__main__":
    load_dotenv(".env")

    init_logger()
    logging.info("Setting up schedule, bot is hot: {}".format(os.getenv("HOT")))
    
    schedule.every().day.at("14:10").do(tweet_reports)
    #schedule.every().day.at("13:24").do(retweet_day_report)
    schedule.every().day.at("13:00").do(check_if_last_day_of_month)

    logging.info("Jobs scheduled: {}".format(schedule.get_jobs()))

    while True:

        schedule.run_pending()
        time.sleep(1)
