# thisProject imports
from app import app, URL, photos, db
from models import User, Tweet, followers
from forms import RegisterForm, LoginForm, TweetForm

# Flask imports
from flask import Flask, render_template, url_for, redirect, request, abort
from flask_login import login_user, login_required, current_user, logout_user
from flask_uploads import UploadSet, configure_uploads, IMAGES

# Non-Flask imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# Routing
@app.route('/')
def index():
    # Handling the GET of the login form
    form = LoginForm()
    return render_template('index.html', form=form, wearehome=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirection to index if GET with /login
    if request.method == 'GET':
        return redirect(url_for('index'))
    # Handling the POST of the login form
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:  # User not available
            return render_template('index.html', form=form, message='The user doesn\'t exist.')
        if check_password_hash(user.password, form.password.data):  # Password match
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile'))
        # Password mismatch
        return render_template('index.html', form=form, message='Wrong password.')
    return redirect(url_for('index'))  # ????


@app.route("/logout")
@login_required
def logout():  # Logout route that works due to Flask-Login
    logout_user()  # Flask-Login function
    return redirect(url_for('index'))


@app.route('/profile', defaults={'username': None})
@app.route('/profile/<username>')
def profile(username):
    # Handling the GET by passing it the profile content
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
    else:
        user = current_user

    tweets = Tweet.query.filter_by(user=user).order_by(
        Tweet.date_created.desc()).all()

    followedBy = user.followed_by.all()

    displayFollow = True
    if current_user == user:
        displayFollow = False
    if current_user in followedBy:
        displayFollow = False

    whoToWatch = User.query.filter(User.id != user.id).order_by(
        db.func.random()).limit(4).all()
    return render_template('profile.html', URL=URL, user=user, followed_by=followedBy, tweets=tweets, current_time=datetime.now(), displayFollow=displayFollow, whoToWatch=whoToWatch)


@app.route('/timeline', defaults={"username": None})
@app.route('/timeline/<username>')
@login_required
def timeline(username):
    # Handling the GET for the tweet form
    form = TweetForm()

    # Get the user id
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
        # Get current users tweets
        userTweets = Tweet.query.filter_by(user=user).order_by(
            Tweet.date_created.desc()).all()
        tweetCount = len(userTweets)
    else:
        user = current_user
        # Get tweets by all the people followed
        tweets = Tweet.query.join(followers, (followers.c.followee_id == Tweet.user_id)).filter(
            followers.c.follower_id == current_user.id).order_by(Tweet.date_created.desc()).all()
        tweetCount = Tweet.query.filter_by(user=user).order_by(
            Tweet.date_created.desc()).count()

    whoToWatch = User.query.filter(User.id != user.id).order_by(
        db.func.random()).limit(4).all()
    return render_template('timeline.html', form=form, URL=URL, tweets=tweets, tweetCount=tweetCount, current_time=datetime.now(), user=user, whoToWatch=whoToWatch)


@app.route('/posttweet', methods=['POST'])
@login_required
def posttweet():
    form = TweetForm()
    if form.validate():  # need only validate() because of only POST
        # Make new tweet object and commit it to the db
        new_tweet = Tweet(user_id=current_user.id,
                          text=form.text.data, date_created=datetime.now())
        db.session.add(new_tweet)
        db.session.commit()
    # Redirect to timeline after posting the tweet
    return redirect(url_for('timeline'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Handling the GET and POST for register form
    form = RegisterForm()
    if form.validate_on_submit():
        # Save image
        image_filename = photos.save(form.image.data)
        # Generate image url ( This uses Flask-Reuploaded, since Flask-Uploads isn't being supported now.)
        image_url = url_for(
            "_uploads.uploaded_file", setname=photos.name, filename=image_filename
        )
        # Make a new user object and commit to the db
        new_user = User(name=form.name.data,
                        username=form.username.data, image=image_url, password=generate_password_hash(form.password.data), joinDate=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)  # Login the user
        return redirect(url_for('profile'))  # Redirect to profile
    # Rendering the page on GET.
    return render_template('register.html', form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()
    # (Below) This is insane, that's all I had to do to add followers.
    current_user.following.append(user_to_follow)
    db.session.commit()
    return redirect(url_for('profile', username=username))


@app.errorhandler(404)
def invalid_route(e):
    return jsonify({'StatusCode': 404, 'message': 'Route not found'})
