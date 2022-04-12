from enum import unique
from operator import pos

from sqlalchemy import Column
from app import db
from datetime import datetime

class Tweets(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body= db.Column(db.String(280),index=True)
    hash_tag = db.Column(db.String(64),index=True)
    score=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,index=True)
    tweet_id=db.Column(db.BigInteger)

    def __repr__(self):
        return '<Tweet with hash_tag {} and score {}>'.format(self.hash_tag,self.score)

    @staticmethod
    def create_tweet(body,hash_tag,date_created,tweet_id):
        try:
            tweet = Tweets(body=body,hash_tag=hash_tag,date_created=date_created,tweet_id=tweet_id)    
            db.session.add(tweet)
            db.session.commit()
        except Exception as err:
            raise err  

    @staticmethod
    def get_all_tweets():
        return Tweets.query.all()

    @staticmethod
    def get_tweets_with_body(body):
        return Tweets.query.filter_by(body=body).first()

    @staticmethod
    def get_tweets_with_tweet_id(tweet_id):
        return Tweets.query.filter_by(tweet_id=tweet_id).first()    

    @staticmethod
    def get_latest_tweet_id(hash_tag):
        return Tweets.query.filter_by(hash_tag=hash_tag).order_by(Tweets.id.desc()).first()   

class CursorPosition(db.Model):
    id=db.Column(db.Integer,primary_key=True)        
    since_id=db.Column(db.BigInteger,default=1)
    key_word=db.Column(db.String(32))

    @staticmethod
    def create_cursor_position(since_id,key_word):
        try:
            position = CursorPosition(since_id=since_id,key_word=key_word)
            db.session.add(position)
            db.session.commit()
        except Exception as err:
            raise err    

    @staticmethod
    def get_cursor_position(key_word):
        return CursorPosition.query.filter_by(key_word=key_word).first()

    @staticmethod
    def get_since_id(key_word):
        position = CursorPosition.get_cursor_position(key_word)
        return position.since_id

    @staticmethod
    def edit_since_id(key_word,since_id):
        position = CursorPosition.get_cursor_position(key_word)
        position.since_id=since_id
        db.session.commit()


