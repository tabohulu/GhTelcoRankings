from itertools import count
from app import app
from app.models import Tweets
from flask import render_template
import app.bots.retwitter_bot as rb
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import tweepy
scheduler = BackgroundScheduler()
api=rb.create_api()
since_ids=[1,1,1,1,1,1]
queries=["mtnghana","#mtnghana","#vodafoneghana","vodafoneghana","airteltigo","#airteltigo"]


@scheduler.scheduled_job(IntervalTrigger(minutes=60))
def print_something():
    
    global since_ids  
    for i in range(len(since_ids)):
        since_id=since_ids[i]

        if since_id==1:
            last_tweet=Tweets.get_latest_tweet_id(queries[i]) 
            if last_tweet is not None:
                since_id=last_tweet.tweet_id
        since_id=rb.capture_tweets(since_id,api,queries[i])
        since_ids[i]=since_id

scheduler.start()

@app.route('/')
@app.route('/index')
def home():
    
    tweets=Tweets.get_all_tweets()
    # print(tweets[0])

    return render_template('index.html',tweets=tweets)