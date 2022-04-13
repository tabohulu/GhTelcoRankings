from app import app
from app.models import Tweets
from app.tasks import get_tweets
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import app.bots.retwitter_bot as rb
from flask import render_template

api=rb.create_api()
queries=["mtnghana","#mtnghana","#vodafoneghana","vodafoneghana","airteltigo","#airteltigo"]

# sched=BlockingScheduler()
sched=BackgroundScheduler()




@app.route('/')
@app.route('/index')
def home():    
    
    return render_template('index.html')

@app.route('/work')    
def work():
    tweets=Tweets.get_unscored_tweets()

    return render_template('work.html',tweets=tweets)


# @sched.scheduled_job('interval',minutes=1,timezone='Asia/Tokyo')
# def print_something():
#     get_tweets()
# sched.start()    