from operator import is_
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import schedule
import time
from DataItem import DataItem
from twitter import tweet_with_image


def main():

    load_dotenv('.env')

    is_hot = True if os.getenv('HOT') == 'True' else False
    
    now = datetime.now()
    tomororrow_0 = datetime(now.year, now.month, now.day+1, 0)
    delta = timedelta(days=2)
    country = "FI"
    tz="Europe/Helsinki"

    #today_0 = datetime(now.year, now.month, now.day, 0)
    #today_15 = datetime(now.year, now.month, now.day, 15)
   

    data_item = DataItem(start=tomororrow_0, end=tomororrow_0+delta, country=country, timezone=tz)
    data_item.get_market_price_dataframe()
    data_item.plot_bar_graph()
    insights = data_item.generate_insights()

    message = f"Sähkön spot-hinnat {data_item.date} (alv 0%)\n"
    message+= f"Keskihinta: {insights['mean']} snt/kWh\n"
    message+= f"Päivän alin: {insights['min']} snt/kWh\n"
    message+=f"Päivän ylin: {insights['max']} snt/kWh\n"
    message+= "#energia #sähkö #hinta #spot"
    print(message)

    if is_hot:
        tweet_with_image(data_item.bar_graph_path, message)


if __name__ == "__main__":
    wake_up_time = os.getenv("WAKE_UP")
    schedule.every().day.at(wake_up_time).do(main)
    while True:
        
        schedule.run_pending()
        time.sleep(1)
        