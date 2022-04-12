# from redis import Redis
# import rq
from app import app
from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.models import CursorPosition
import app.bots.retwitter_bot as rb

api=rb.create_api()
queries=["mtnghana","#mtnghana","#vodafoneghana","vodafoneghana","airteltigo","#airteltigo"]

scheduler = BackgroundScheduler()
sched=BlockingScheduler()




@sched.scheduled_job('interval',minutes="3")
def print_something():
     print('This job is run every three minutes.')
    # for query in queries:
    #     cursor_pos=CursorPosition.get_cursor_position(query)
    #     if cursor_pos is None:
    #         CursorPosition.create_cursor_position(1,query)
    #         since_id=1
    #     since_id=CursorPosition.get_since_id(query)   
    #     since_id=rb.capture_tweets(since_id,api,query)
    #     CursorPosition.edit_since_id(query,since_id)
    # get_tweets()
#    queue= rq.Queue('rankings-tasks',connection=Redis.from_url(app.config['REDISTOGO_URL'])) 
#    job=queue.enqueue('app.tasks.get_tweets')
    

sched.start()