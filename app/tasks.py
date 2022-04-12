import time
from app.models import CursorPosition
import app.bots.retwitter_bot as rb

api=rb.create_api()
queries=["mtnghana","#mtnghana","#vodafoneghana","vodafoneghana","airteltigo","#airteltigo"]

def example(seconds):
    print('Starting task')
    for i in range(seconds):
        print(i)
        time.sleep(1)
    print('Task completed')

def get_tweets(): 
    for query in queries:
        cursor_pos=CursorPosition.get_cursor_position(query)
        if cursor_pos is None:
            CursorPosition.create_cursor_position(1,query)
            since_id=1
        since_id=CursorPosition.get_since_id(query)   
        since_id=rb.capture_tweets(since_id,api,query)
        CursorPosition.edit_since_id(query,since_id)    