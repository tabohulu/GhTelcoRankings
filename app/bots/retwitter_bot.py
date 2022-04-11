import tweepy
import os
from config import Config
from app.models import Tweets
def create_api():
    consumer_key = Config.CONSUMER_KEY
    consumer_secret = Config.CONSUMER_SECRET
    access_token = Config.ACCESS_TOKEN
    access_token_secret = Config.ACCESS_SECRET

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        api.verify_credentials()        
    except Exception as e :
        raise e 
    return api  

def capture_tweets(since_id,api,query):
    new_since_id = since_id
    print(new_since_id)
    api.mentions_timeline()
    for tweet in tweepy.Cursor(api.search_tweets,since_id=since_id,q=query,count=10,tweet_mode="extended").items(100):
        new_since_id = max(tweet.id, new_since_id)
        print('user:{} tweets {}'.format(tweet.user.name,tweet.full_text))
        db_value=Tweets.get_tweets_with_body(tweet.full_text)
        if db_value is None:
            Tweets.create_tweet(body=tweet.full_text,hash_tag=query,date_created=tweet.created_at,tweet_id=tweet.id)
    print("====================================")
    return new_since_id
    