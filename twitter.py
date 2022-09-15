import tweepy
import os

def twitter_api():
    print("Setting up twitter API connection..")
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



def tweet_with_image(image_path: str, message: str):
    print("Tweeting..")
    api = twitter_api()
    api.update_status_with_media(message ,image_path)
    os.remove(image_path)


