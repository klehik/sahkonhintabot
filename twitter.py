import tweepy
import os
import logging

def twitter_api():
    # Twitter API v1
    logging.info("Setting up twitter API v1 connection..")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_KEY_SECRET")

    auth = tweepy.OAuth1UserHandler(
        consumer_key, 
        consumer_secret, 
        access_token,
        access_token_secret)
    api = tweepy.API(auth)
    return api

def twitter_client():
    # Twitter API v2

    logging.info("Setting up twitter API v2 connection..")

    bearer = os.getenv("TWITTER_BEARER")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_KEY_SECRET")

    client = tweepy.Client(bearer, consumer_key, consumer_secret, access_token, access_token_secret)
   
    return client

def upload_media(files):
    media_ids = []
    api = twitter_api()
    logging.info("Uploading media: {}".format(files))
    for file in files:
        media = api.media_upload(file)
        media_ids.append(media.media_id)
    return media_ids


def tweet_with_multi_image(media_ids, message):
    api=twitter_api()
    return api.update_status(status=message, media_ids=media_ids)
    

def reply_to_tweet(message, image_path, tweet_id):
    api = twitter_api()
    logging.info("Replying to tweet: {}".format(tweet_id))
    return api.update_status_with_media(status=message ,filename=image_path, in_reply_to_status_id=tweet_id)



def tweet_with_image(image_path: str, message: str):
    api = twitter_api()
    logging.info("Tweeting with image: {}".format(image_path))
    return api.update_status_with_media(message ,image_path)
    
    #os.remove(image_path)


def retweet(id):
    api = twitter_api()
    logging.info("Retweeting, tweet id: {}".format(id))
    api.retweet(id)
    

def get_tweet(id):

    client = twitter_client()

    res = client.get_tweet(id, expansions='author_id,in_reply_to_user_id,referenced_tweets.id', user_fields='name,username', tweet_fields='author_id,conversation_id,created_at,in_reply_to_user_id,referenced_tweets')

    #print(res.includes['users'], res.data.conversation_id)
    return res

def get_conversation_id(id):
    tweet = get_tweet(id)
    return tweet.data.conversation_id


def get_users_from_tweet(id):
    tweet = get_tweet(id)
    return tweet.includes['users']

