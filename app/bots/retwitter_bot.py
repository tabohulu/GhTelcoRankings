import tweepy
import os
from app.models import Tweets
def create_api():
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)

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
        # print('user:{} tweets {}'.format(tweet.user.name,tweet.full_text))
        body=tweet.full_text
        if len(body)>280:
            body=body[0:279]
        Tweets.create_tweet(body=body,hash_tag=query,date_created=tweet.created_at,tweet_id=tweet.id)
    print("====================================")
    return new_since_id
    