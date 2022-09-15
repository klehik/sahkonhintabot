from dotenv import load_dotenv

from datetime import datetime, timedelta
import schedule
import time
from DataItem import DataItem
from twitter import tweet_with_image


def main():


    load_dotenv('.env')


    now = datetime.now()
    today_0 = datetime(now.year, now.month, now.day, 0)
    tomororrow_0 = datetime(now.year, now.month, now.day+1, 0)
    #today_15 = datetime(now.year, now.month, now.day, 15)
    delta = (timedelta(days=2))
    country = "FI"
    tz='Europe/Helsinki'

    data_item = DataItem(start=today_0, end=tomororrow_0, country=country, timezone=tz)

    data_item.get_market_price_dataframe()
    
    data_item.plot_bar_graph()

    insights = data_item.generate_insights()
    hashtags = "#energia #sähkö #hinta #spot"
    message = f"Sähkön spot-hinnat {data_item.date} (alv 0%)\nKeskihinta: {insights['mean']} snt/kWh\nPäivän alin: {insights['min']} snt/kWh\nPäivän ylin: {insights['max']} snt/kWh\n{hashtags}"
    print(message)
    tweet_with_image(data_item.bar_graph_path, message)


if __name__ == "__main__":
    schedule.every().day.at("15:00").do(main)
    
    while True:
        
        schedule.run_pending()
        time.sleep(1)