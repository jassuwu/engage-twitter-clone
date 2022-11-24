# thisProject imports
from app import app, URL, photos, db
from models import User, Tweet
from forms import RegisterForm, LoginForm, TweetForm

# Flask imports
from flask import Flask, render_template, url_for, redirect, request
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
    return render_template('index.html', form=form)


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


@app.route('/profile')
def profile():
    # Handling the GET by passing it the profile content
    return render_template('profile.html', URL=URL, current_user=current_user)


@app.route('/timeline')
@login_required
def timeline():
    # Handling the GET for the tweet form
    form = TweetForm()

    # Get the user id
    user_id = current_user.id
    # Get current users tweets
    tweets = Tweet.query.filter_by(user_id=user_id).order_by(
        Tweet.date_created.desc()).all()
    return render_template('timeline.html', form=form, URL=URL, tweets=tweets, current_time=datetime.now())


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
        return redirect(url_for('login'))  # Redirect to login
    # Rendering the page on GET.
    return render_template('register.html', form=form)
