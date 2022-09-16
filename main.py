from operator import is_
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import schedule
import time
from DataItem import DataItem
from twitter import tweet_with_image
from utils import compile_message


def main():

    load_dotenv(".env")

    is_hot = True if os.getenv("HOT") == 'True' else False
    

    now = datetime.now()
    tomororrow_0 = datetime(now.year, now.month, now.day+1, 0)
    delta = timedelta(days=1)
    country = "FI"
    tz="Europe/Helsinki"
   

    data_item = DataItem(start=tomororrow_0, end=tomororrow_0+delta, country=country, timezone=tz)
    data_item.get_market_price_dataframe()
    data_item.plot_bar_graph()
    
    message = compile_message(data_item)

    print(message, len(message))

    if is_hot:
        tweet_with_image(data_item.bar_graph_path, message)
    else:
        print("The bot is not hot")

if __name__ == "__main__":
    
    schedule.every().day.at("15:00").do(main)
    
    while True:
        
        schedule.run_pending()
        time.sleep(1) 
        