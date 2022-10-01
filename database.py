import pymongo
import os
from dotenv import load_dotenv


# A simple database to keep track of conversations the bot has already participated



def get_id_db():
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client.sahkonhintabot
    ids = db.conversation_ids

    return ids


def add_tweet(text, bot_replied):
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client.sahkonhintabot
    tweets = db.tweets

    tweet_document = {
        "text": text,
        "bot_replied": bot_replied
    }
    res = tweets.insert_one(tweet_document)
    print(res)


def get_tweets():

    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client.sahkonhintabot
    tweets = db.tweets

    return tweets


def add_id(id):

    ids = get_id_db()
    

    id_document = {
        "conversation_id": id
    }
    res = ids.insert_one(id_document)
    print(res)

def find_id(id):

    ids = get_id_db()

    id = ids.find_one({"conversation_id": id})

    return id

def add_insights(data_item, tweet_id):

    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client.sahkonhintabot
    insights = db.insights

    in_database = insights.find_one({"date": data_item.timeframe_str})
    print(in_database)
    if not in_database:

        insights_document = data_item.insights


        insights_document['date'] = data_item.timeframe_str
        insights_document['tweet_id'] = tweet_id
           

        res = insights.insert_one(insights_document)
        print(res)

def get_insight(date):

    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client.sahkonhintabot
    insights = db.insights

    insight = insights.find_one({"date": date})
    
    return insight
    

def delete_id_db():
    load_dotenv('.env')
    ids = get_id_db()
    ids.delete_many({})


