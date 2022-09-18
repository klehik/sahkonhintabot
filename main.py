from operator import is_
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import schedule
import time
from DataItem import DataItem
from twitter import tweet_with_image
from utils import compile_message
import tweepy

from TweetResponder import TweetResponder

def main():

    

    is_hot = True if os.getenv("HOT") == 'True' else False
    
   
    now = datetime.now()
    delta = timedelta(days=1)
    tomorrow = datetime(now.year, now.month, now.day, 0) + delta

    country = "FI"
    tz="Europe/Helsinki"
    
    
    data_item = DataItem(start=tomorrow, end=tomorrow+delta, country=country, timezone=tz)
    data_item.get_market_price_dataframe()
    # TODO: bar_graph_path = data_item.plot_bar_graph
    if not data_item.dataframe.empty:
        data_item.plot_bar_graph()
    
        message = compile_message(data_item)

        print(message, len(message))
        if is_hot:
            tweet_with_image(data_item.bar_graph_path, message)
        else:
            print("The bot is not hot")
    else:
        print("dataframe empty")


    

if __name__ == "__main__":
    load_dotenv(".env")
    
    schedule.every().day.at("14:30").do(main)

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
    responder.filter(tweet_fields="conversation_id")

    
    
    while True:
        
        schedule.run_pending()
        time.sleep(1)
        