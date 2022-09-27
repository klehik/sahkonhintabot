
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import schedule
import time
from DataItem import DataItem
from twitter import tweet_with_image, retweet
from utils import compile_day_ahead_message
import tweepy
import database
from entso_api import *
from TweetResponder import TweetResponder





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

        
        print(message, len(message))
        if is_hot:
            res = tweet_with_image(data_item.bar_graph_path, message)
            tweet_id = res['id']
            database.add_insights(data_item, tweet_id)
        else:
            print("The bot is not hot")
    else:
        print("dataframe empty")
        time.sleep(600)
        tweet_day_ahead_report()



def tweet_weekly_report():
    now = datetime.now()
    end = datetime(now.year, now.month, now.day)
    data_item = get_7(end=end)
    
    #graph_settings = {"hourly": False, "label_rotation": 0, "bars_from_start": 2}
    graph_settings = {"hourly": True, "label_rotation": 0, "bars_from_start": 32}
    
    data_item.plot_bar_graph(graph_settings)
    print(data_item.insights)
    #database.add_insights(data_item)


def tweet_monthly_report():
    now = datetime.now()
    end = datetime(now.year, now.month, now.day+1)
    data_item = get_28(end=end)
    
    graph_settings = {"hourly": False, "label_rotation": 45, "bars_from_start": 6}
    #graph_settings = {"hourly": True, "label_rotation": 45, "bars_from_start": 120}
    
    data_item.plot_bar_graph(graph_settings)
    print(data_item.insights)
    
    #tweet_monthly_report()
    #tweet_weekly_report()
    #tweet_day_ahead_report()
    
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
    
    schedule.every().day.at("14:10").do(tweet_day_ahead_report)
    schedule.every().day.at("07:00").do(retweet_day_report)

    bearer = os.getenv("TWITTER_BEARER")

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
    responder.filter(tweet_fields="conversation_id", threaded=True)

    
    
    while True:
        
        schedule.run_pending()
        time.sleep(1)
        