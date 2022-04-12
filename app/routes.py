from app import app
from app.models import Tweets
from flask import render_template
# from redis import Redis
# import rq
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.interval import IntervalTrigger

# scheduler = BackgroundScheduler()

# @scheduler.scheduled_job(IntervalTrigger(minutes=5))
# def print_something():
#    queue= rq.Queue('rankings-tasks',connection=Redis.from_url('redis://')) 
#    job=queue.enqueue('app.tasks.get_tweets')
    

# scheduler.start()

@app.route('/')
@app.route('/index')
def home():
    
    tweets=Tweets.get_all_tweets()
    # print(tweets[0])

    return render_template('index.html',tweets=tweets)