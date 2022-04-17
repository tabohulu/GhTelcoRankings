from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import BIGINT
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique = True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20))#admin/#eval
    sentiments = db.relationship('Sentiment',backref='author',lazy ='dynamic')#User.sentiments returns all sentiments associated with the user


    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)    

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

class Sentiment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sentiment_score=db.Column(db.Integer)
    user_id =  db.Column(db.Integer,db.ForeignKey('user.id'))#Sentiment.author return the user who assigned the sentiment
    tweet_id = db.Column(db.Integer,db.ForeignKey('tweets.id'))#Sentiment.subject return the tweet to which the sentiment is assigned


    def __repr__(self):
        return 'sentiment score of {} for tweet with id {} by evaluator {}'.format(self.sentiment_score,self.tweet_id,self.author.username)

      
    @staticmethod
    def create_sentiment(sentiment_score,user,tweet):
        sentiment =Sentiment(sentiment_score=sentiment_score,author=user,subject=tweet)
        db.session.add(sentiment)
        db.session.commit()

    @staticmethod
    def delete_all_sentiments():
        sentiments=Sentiment.query.all()
        for sentiment in sentiments:
            print(sentiment)
            db.session.delete(sentiment)
        db.session.commit()  

    @staticmethod
    def get_sentiments_by_score(score):
        sentiments=Sentiment.query.filter(Sentiment.sentiment_score==score).all()
        return sentiments 

    @staticmethod
    def get_total_sentiments_with_score(score):
        return Sentiment.query.filter(Sentiment.sentiment_score==score).count()            



class Tweets(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body= db.Column(db.String(280),index=True)
    hash_tag = db.Column(db.String(64),index=True)
    score=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,index=True)
    tweet_id=db.Column(BIGINT)
    score_assigned=db.Column(db.Boolean,default=False)
    sentiments= db.relationship('Sentiment',backref='subject',lazy='dynamic')

    def __repr__(self):
        return '<Tweet with hash_tag {} and score {}>'.format(self.hash_tag,self.score)

    @staticmethod
    def create_tweet(body,hash_tag,date_created,tweet_id):
        try:
            if Tweets.get_tweets_with_body(body) is None:
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
    def get_scored_tweets():
        return Tweets.query.filter_by(score_assigned=True).all()

    @staticmethod
    def get_unscored_tweets():
        return Tweets.query.filter_by(score_assigned=False).all() 

    @staticmethod
    def get_unscored_tweets_lim(user,limit):
        # limit1=int(limit/2)        
        # tweets2 = Tweets.query.filter(Tweets.sentiments!=None,Sentiment.author!=user).join(Tweets.sentiments).order_by(Tweets.date_created).limit(limit1).all()
        tweets1 = Tweets.query.filter((Tweets.sentiments==None)).order_by(Tweets.date_created).limit(limit).all()
        return tweets1#+tweets2


    @staticmethod
    def get_tweets_with_tweet_id(tweet_id):
        return Tweets.query.filter_by(tweet_id=tweet_id).first()    

    @staticmethod
    def get_tweets_by_id(id):
        return Tweets.query.filter_by(id=id).first()

    @staticmethod
    def get_latest_tweet_id(hash_tag):
        return Tweets.query.filter_by(hash_tag=hash_tag).order_by(Tweets.id.desc()).first()   

    @staticmethod
    def get_tweets_count():
        rows = db.session.query(Tweets).filter((Tweets.sentiments==None)).count()
        return rows

class CursorPosition(db.Model):
    id=db.Column(db.Integer,primary_key=True)        
    since_id=db.Column(BIGINT,default=1)
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

