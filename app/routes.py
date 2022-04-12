from app import app
from app.models import Tweets,CursorPosition
from flask import render_template


@app.route('/')
@app.route('/index')
def home():
    
    tweets=Tweets.get_all_tweets()
    # print(tweets[0])

    return render_template('index.html',tweets=tweets)