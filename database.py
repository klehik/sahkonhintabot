import pymongo
import os
from dotenv import load_dotenv
import logging

'''A simple database to save and load tweet ids for retweeting'''



def add_tweet(report, tweet_id):
    logging.info("Saving tweet id for report on {}".format(report.timeframe_str))
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client.sahkonhintabot
    insights = db.insights

    in_database = insights.find_one({"date": report.timeframe_str})
    print(in_database)
    if not in_database:

        insights_document = {}


        insights_document['date'] = report.timeframe_str
        insights_document['tweet_id'] = tweet_id
           

        res = insights.insert_one(insights_document)
        print(res)

def get_tweet(date):
    logging.info("Searching tweet id for report on {}".format(date))
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client.sahkonhintabot
    insights = db.insights

    insight = insights.find_one({"date": date})
    
    return insight
    

