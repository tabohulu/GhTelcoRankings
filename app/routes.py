from crypt import methods
from app import app
from app.models import Tweets, User
from app.forms import LoginForm
from app.tasks import get_tweets
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import app.bots.retwitter_bot as rb
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user,logout_user

api=rb.create_api()
queries=["mtnghana","#mtnghana","#vodafoneghana","vodafoneghana","airteltigo","#airteltigo"]

# sched=BlockingScheduler()
sched=BackgroundScheduler()


@app.route('/')
@app.route('/index')
def index():    
    
    return render_template('index.html')

@app.route('/work')    
def work():
    tweets=Tweets.get_unscored_tweets()

    return render_template('work.html',tweets=tweets)

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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
# @sched.scheduled_job('interval',minutes=1,timezone='Asia/Tokyo')
# def print_something():
#     get_tweets()
# sched.start()    