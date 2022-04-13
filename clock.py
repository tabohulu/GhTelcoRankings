from app import app
from app.tasks import get_tweets
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.models import CursorPosition
import app.bots.retwitter_bot as rb

api=rb.create_api()
queries=["mtnghana","#mtnghana","#vodafoneghana","vodafoneghana","airteltigo","#airteltigo"]

sched=BlockingScheduler()


@sched.scheduled_job('interval',minutes=60,timezone='Asia/Tokyo')
def print_something():
    get_tweets()
    

sched.start()