

from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import schedule
import time
from twitter import tweet_with_image, retweet, reply_to_tweet, upload_media, tweet_with_multi_image
from utils import get_days_in_month
from message import *
import tweepy
import database
from entso_api import *
from TweetResponder import TweetResponder


def check_if_last_day_of_month():
    now = datetime.now()
    is_last_day_of_month = True if now.day == get_days_in_month(now) else False

    if is_last_day_of_month:
       
        tweet_monthly_report(now)



def reply_additional_info(data_item, first_tweet_id):
    

    data_item_7 = data_item.avg_7_day
    graph_settings_7 = {"hourly": True, "label_rotation": 0, "bars_from_start": 32}
    data_item_7.plot_bar_graph(graph_settings_7)

    data_item_28 = data_item.avg_28_day
    graph_settings_28 = {"hourly": False, "label_rotation": 45, "bars_from_start": 6, "bar_label_font_size": 6}
    data_item_28.plot_bar_graph(graph_settings_28)

    
    print(data_item_7.bar_graph_path)
    print(data_item_28.bar_graph_path)
    
    
    time.sleep(10)
    avg_7_message = compile_7_day_reply_message(data_item_7)
    res7 = reply_to_tweet(avg_7_message, data_item_7.bar_graph_path, first_tweet_id)
    time.sleep(10)
    avg_28_message = compile_28_day_reply_message(data_item_28)
    res_28 = reply_to_tweet(avg_28_message, data_item_28.bar_graph_path, res7.id)
    
    print(avg_7_message)
    print(avg_28_message)


    


def tweet_day_ahead_report():

    is_hot = True if os.getenv("HOT") == 'True' else False

    now = datetime.now()
    one_day = timedelta(days=1)
    tomorrow = now+one_day  
    data_item = get_day(tomorrow)
    

    if not data_item.dataframe.empty:
    
        graph_settings = {"bar_labels": True}
        data_item.plot_bar_graph(graph_settings)
        message = compile_day_ahead_message(data_item)
        reply_additional_info(data_item)
        
        print(message, len(message))
        if is_hot:

            today_img_path = f"./images/{now.day}.{now.month}.{now.year}.png"
            media_ids = upload_media(files=[data_item.bar_graph_path, today_img_path])
            res = tweet_with_multi_image(media_ids=media_ids, message=message)
            tweet_id = res.id
            reply_additional_info(data_item, tweet_id)
            database.add_insights(data_item, tweet_id)

        else:
            print("The bot is not hot")
    else:
        print("dataframe empty")
        time.sleep(600)
        tweet_day_ahead_report()


def tweet_monthly_report(now):

    is_hot = True if os.getenv("HOT") == 'True' else False

    one_month = timedelta(days=35)

    # current month
    data_item_current = get_month(now)

    # previous month
    data_item_previous = get_month(now-one_month)
    
    
    graph_settings = {"hourly": False, "label_rotation": 45, "bars_from_start": 6, "bar_label_font_size": 6}
    #graph_settings = {"hourly": True, "label_rotation": 45, "bars_from_start": 120}

    data_item_current.plot_bar_graph(graph_settings)
    message = compile_monthly_message(data_item_current, data_item_previous)

    if is_hot:
        res = tweet_with_image(data_item_current.bar_graph_path, message)
        tweet_id = res.id
        database.add_insights(data_item_current, tweet_id)
    
    else:
        print("The bot is not hot")


def tweet_weekly_report():

    is_hot = True if os.getenv("HOT") == 'True' else False

    one_week = timedelta(days=7)
    
    now = datetime.now()
    

    # current week
    data_item_current = get_week(now)

    # previous week
    data_item_previous = get_week(now-one_week)
    
    #graph_settings = {"hourly": False, "label_rotation": 0, "bars_from_start": 2}
    graph_settings = {"hourly": True, "label_rotation": 0, "bars_from_start": 32}
    
    data_item_current.plot_bar_graph(graph_settings)
    
    message = compile_weekly_message(data_item_current, data_item_previous)
    print(message)

    if is_hot:
        res = tweet_with_image(data_item_current.bar_graph_path, message)
        tweet_id = res.id
        database.add_insights(data_item_current, tweet_id)
    
    else:
        print("The bot is not hot")



    
def retweet_day_report():
    now = datetime.now()
    date = f"{str(now.day)}.{str(now.month)}.{str(now.year)}"
    insight = database.get_insight(date)
    if insight:
        id = insight['tweet_id']
        retweet(id)
    else: 
        print(f"insight '{date}' not found from database")   


    

if __name__ == "__main__":
    load_dotenv(".env")
    tweet_day_ahead_report()
    """ schedule.every().day.at("14:10").do(tweet_day_ahead_report)
    schedule.every().day.at("07:00").do(retweet_day_report)
    schedule.every().day.at("11:00").do(check_if_last_day_of_month)
    schedule.every().sunday.at("12:00").do(tweet_weekly_report) """

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

    
    
    """ while True:
        
        schedule.run_pending()
        time.sleep(1) """
        