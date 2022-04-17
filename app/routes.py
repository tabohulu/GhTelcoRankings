from app import app,db
from app.models import Sentiment, Tweets, User
from app.forms import LoginForm
from apscheduler.schedulers.background import BackgroundScheduler
import app.bots.retwitter_bot as rb
from flask import flash, redirect, render_template, url_for,request
from flask_login import current_user, login_user,logout_user, login_required
from werkzeug.urls import url_parse

api=rb.create_api()
queries=["mtnghana","#mtnghana","#vodafoneghana","vodafoneghana","airteltigo","#airteltigo"]
sched=BackgroundScheduler()
limit=20


@app.route('/')
@app.route('/home')
def index(): 
    overview={} 
    overview['positive']=Sentiment.get_total_sentiments_with_score(1)
    overview['neutral']=Sentiment.get_total_sentiments_with_score(0)
    overview['negative']=Sentiment.get_total_sentiments_with_score(-1)
    return render_template('index.html',title="Home",overview=overview)

@app.route('/work')
@login_required    
def work():
    tweets=Tweets.get_unscored_tweets_lim(current_user, limit=limit)
    total_tweets= Tweets.get_tweets_count()
    return render_template('work.html',tweets=tweets,title="Work", count = total_tweets)

@app.route('/work_submitted',methods=['GET','POST'])
def work_submitted():
    for key in request.form.keys():
        tweet=Tweets.get_tweets_by_id(int(key.split('-')[0]))
        Sentiment.create_sentiment(sentiment_score=int(request.form[key]),user=current_user,tweet=tweet)        
    return redirect(url_for('work'))



@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')  
        
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/create_admin')
def create_admin():
    username='bohuluAdmin'
    email='bohulukwame@gmail.com'
    password="married@Thirty3"
    if User.query.filter(User.username==username,User.user_type=='admin').first() is None:
        user=User(username=username,email=email,user_type='admin')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return 'user created'
    return 'user already exists'      
# @sched.scheduled_job('interval',minutes=1,timezone='Asia/Tokyo')
# def print_something():
#     get_tweets()
# sched.start()    