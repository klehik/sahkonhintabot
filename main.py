

from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import schedule
import time
from twitter import tweet_with_image, retweet, reply_to_tweet, upload_media, tweet_with_multi_image
from utils import get_days_in_month
from message import *
import database
from report_generators import *
from TweetResponder import TweetResponder
from log import init_logger
import logging



def check_if_last_day_of_month():
    now = datetime.now()
    is_last_day_of_month = True if now.day == get_days_in_month(now) else False

    if is_last_day_of_month:
       
        tweet_monthly_report(now)



def reply_additional_info(report, first_tweet_id):
    
    logging.info("Generating 7-day report")
    report_7 = report.avg_7_day
    graph_settings_7 = {"hourly": True, "label_rotation": 0, "bars_from_start": 32}
    report_7.plot_bar_graph(graph_settings_7)

    logging.info("Generating 28-day report")
    report_28 = report.avg_28_day
    graph_settings_28 = {"hourly": False, "label_rotation": 45, "bars_from_start": 6, "bar_label_font_size": 6}
    report_28.plot_bar_graph(graph_settings_28)
    
    avg_7_message = compile_7_day_reply_message(report_7)
    res7 = reply_to_tweet(avg_7_message, report_7.bar_graph_path, first_tweet_id)
    
    avg_28_message = compile_28_day_reply_message(report_28)
    res_28 = reply_to_tweet(avg_28_message, report_28.bar_graph_path, res7.id)
    
    logging.info("7-day message: {}".format(avg_7_message))
    logging.info("28-day message: {}".format(avg_28_message))
    
   

def tweet_day_ahead_report():
    logging.info("Generating day-ahead report")
    is_hot = True if os.getenv("HOT") == 'True' else False

    now = datetime.now()
    one_day = timedelta(days=1)
    tomorrow = now+one_day  
    report = generate_day_report(tomorrow)
    

    if not report.dataframe.empty:
        
        graph_settings = {"bar_labels": True, "label_rotation": 0, "bars_from_start": 5, "bar_label_font_size": 8}
        report.plot_bar_graph(graph_settings)
        message = compile_day_ahead_message(report)
        
        
        
        logging.info("Day-ahead message: \n{}".format(message))
    
        if is_hot:
            res = tweet_with_image(report.bar_graph_path, message)
            tweet_id = res.id
            reply_additional_info(report, tweet_id)
            database.add_insights(report, tweet_id)

        else:
            print("The bot is not hot")
    else:
        logging.info("Dataframe is empty, trying again in 10 minutes")
        time.sleep(600)
        tweet_day_ahead_report()


def tweet_monthly_report(now):
    logging.info("Generating monthly report")
    is_hot = True if os.getenv("HOT") == 'True' else False

    one_month = timedelta(days=35)

    # current month
    report_current = generate_month_report(now)

    # previous month
    report_previous = generate_month_report(now-one_month)
    
    
    graph_settings = {"hourly": False, "label_rotation": 45, "bars_from_start": 6, "bar_label_font_size": 6}
    #graph_settings = {"hourly": True, "label_rotation": 45, "bars_from_start": 120}

    report_current.plot_bar_graph(graph_settings)
    message = compile_monthly_message(report_current, report_previous)

    if is_hot:
        res = tweet_with_image(report_current.bar_graph_path, message)
        tweet_id = res.id
        database.add_insights(report_current, tweet_id)
    
    else:
        print("THE BOT IS NOT HOT")


def tweet_weekly_report():
    logging.info("Generating weekly report")
    is_hot = True if os.getenv("HOT") == 'True' else False

    one_week = timedelta(days=7)
    
    now = datetime.now()
    

    # current week
    report_current = generate_week_report(now)

    # previous week
    report_previous = generate_week_report(now-one_week)
    
    #graph_settings = {"hourly": False, "label_rotation": 0, "bars_from_start": 2}
    graph_settings = {"hourly": True, "label_rotation": 0, "bars_from_start": 32}
    
    report_current.plot_bar_graph(graph_settings)
    
    message = compile_weekly_message(report_current, report_previous)
    print(message)

    if is_hot:
        res = tweet_with_image(report_current.bar_graph_path, message)
        tweet_id = res.id
        database.add_insights(report_current, tweet_id)
    
    else:
        print("The bot is not hot")



    
def retweet_day_report():
    now = datetime.now()
    date = f"{str(now.day)}.{str(now.month)}.{str(now.year)}"
    insight = database.get_insight(date)
    if insight:
        logging.info("Searching tweet id for day-ahead report on {}".format(date))
        id = insight['tweet_id']
        retweet(id)
    else: 
        logging.info("Tweet id on {} not found from database".format(date))   


    

if __name__ == "__main__":
    load_dotenv(".env")
     
    init_logger()
    logging.info("Setting up schedule, bot is hot: {}".format(os.getenv("HOT")))

    schedule.every().day.at("14:10").do(tweet_day_ahead_report)
    schedule.every().day.at("07:00").do(retweet_day_report)
    schedule.every().day.at("11:00").do(check_if_last_day_of_month)
    #schedule.every().sunday.at("12:00").do(tweet_weekly_report)

    logging.info("Jobs scheduled: {}".format(schedule.get_jobs()))
    
    """ bearer = os.getenv("TWITTER_BEARER")

    # clear stream rules
    a = tweepy.StreamingClient(bearer)
    for asd in a.get_rules()[0]:
        a.delete_rules(asd.id)

    print(a.get_rules())
    
    responder = TweetResponder(bearer)

    # add new rules
    rule = tweepy.StreamRule(value="sähkö lang:fi -is:retweet -is:quote")
    responder.add_rules(rule)
    print(responder.get_rules())
    responder.filter(tweet_fields="conversation_id", threaded=True) """

    
    
    while True:
        
        schedule.run_pending()
        time.sleep(1) 
        