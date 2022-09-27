from twitter import twitter_api, twitter_client, get_conversation_id, get_users_from_tweet
from dotenv import load_dotenv
import tweepy
import os
import database
from utils import compile_reply
from os import system



class TweetResponder(tweepy.StreamingClient):

    
    
    def on_tweet(self, tweet):
        print(tweet.data)
        tweet.text = tweet.text.lower()

        if self.tweet_has_keywords(tweet) and not self.replying_to_self(tweet):
            #client = twitter_client()
            message, img_path = compile_reply()
            #api = twitter_api()
            #media = api.media_upload(img_path)
            print(img_path)
            #client.create_tweet(in_reply_to_tweet_id=tweet.id, text=message, media_ids=[media.media_id])
            print('Replying to tweet')
            
        else:
            database.add_tweet(tweet.text, False)


 
    def replying_to_self(self, tweet):
        conversation_id = get_conversation_id(tweet.id)

        users_original = get_users_from_tweet(conversation_id)
        users_tweet = get_users_from_tweet(tweet.id)

        bots = filter(lambda user: 'bot' in user['username'] or 'bot' in user['name'], users_original + users_tweet)
        
        if len(list(bots)) == 0:
            print('no bots or self')
            return False
        else:
            print('bots or self found')
            return True


    def tweet_has_keywords(self, tweet):

        # kallis sähkö, 
        keywords = ['kwh']
        is_match = False
        tweet.text = tweet.text.lower()
        if 'sähkö' in tweet.text:
            for keyword in keywords:
                if keyword in tweet.text:
                    print(keyword)
                    is_match = True
            if is_match:
                database.add_tweet(tweet.text, True)
                if database.find_id(tweet.conversation_id):
                    print("The bot has replied already in this conversation")
                else:
                    print("Conversation not seen before")
                    database.add_id(tweet.conversation_id)
                    return True
                    
                print(tweet.text)
            else:
                print('NO keyword MATCH', tweet.text)
        else:
            print('NO sähkö MATCH', tweet.text)
        print(50*'-')
        return False




