from app import app
from app.models import Tweets,CursorPosition
from flask import render_template
import app.bots.retwitter_bot as rb
# from redis import Redis
# import rq
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
api=rb.create_api()
queries=["mtnghana","#mtnghana","#vodafoneghana","vodafoneghana","airteltigo","#airteltigo"]
scheduler = BackgroundScheduler()

@scheduler.scheduled_job(IntervalTrigger(minutes=1,timezone="Asia/Tokyo"))
def print_something():
    for query in queries:
        cursor_pos=CursorPosition.get_cursor_position(query)
        if cursor_pos is None:
            CursorPosition.create_cursor_position(1,query)
            since_id=1
        since_id=CursorPosition.get_since_id(query)   
        since_id=rb.capture_tweets(since_id,api,query)
        CursorPosition.edit_since_id(query,since_id)

# @scheduler.scheduled_job(IntervalTrigger(minutes=5))
# def print_something():
#    queue= rq.Queue('rankings-tasks',connection=Redis.from_url('redis://')) 
#    job=queue.enqueue('app.tasks.get_tweets')
    

scheduler.start()

@app.route('/')
@app.route('/index')
def home():
    
    tweets=Tweets.get_all_tweets()
    # print(tweets[0])

    return render_template('index.html',tweets=tweets)