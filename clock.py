# from redis import Redis
# import rq
from app import app
from app.tasks import get_tweets
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = BackgroundScheduler()



@scheduler.scheduled_job(IntervalTrigger(minutes=1))
def print_something():
    get_tweets()
#    queue= rq.Queue('rankings-tasks',connection=Redis.from_url(app.config['REDISTOGO_URL'])) 
#    job=queue.enqueue('app.tasks.get_tweets')
    

scheduler.start()