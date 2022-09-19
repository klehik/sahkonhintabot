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


def delete_db():
    load_dotenv('.env')
    ids = get_id_db()
    ids.delete_many({})


