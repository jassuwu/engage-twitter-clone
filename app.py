# Flask imports
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

# Non-flask imports
from wtforms import StringField, IntegerField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

URL = "http://localhost:5000"

# Initalize the app
app = Flask(__name__)
# XAMPP db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost:3306/engage'
app.config['SECRET_KEY'] = 'dev'
app.config['UPLOADED_PHOTOS_DEST'] = 'images'  # Flask-Reupload
app.config["UPLOADS_AUTOSERVE"] = True  # Flask-Reuploaded

# Flask-login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # default view when unauthorized
# Flask-Reuploaded
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Initialize the db and migrate
db = SQLAlchemy(app)
# Flask-Migrate
migrate = Migrate(app, db)


class User(UserMixin, db.Model):  # User Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30), unique=True)
    image = db.Column(db.String(100))
    password = db.Column(db.Text)
    # 2. added joinDate when making profile route
    joinDate = db.Column(db.DateTime)
    # 3. added tweets backref when making the timeline
    tweets = db.relationship('Tweet', backref='user', lazy='dynamic')


class Tweet(db.Model):  # Tweet Model
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.Text)
    date_created = db.Column(db.DateTime)


# Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegisterForm(FlaskForm):  # Regsitration Form
    name = StringField('Full name', validators=[InputRequired(
        'A full name is required for regsitration.'), Length(min=8, max=100, message='name should be within 8 and 100 characters.')])
    username = StringField('Username', validators=[InputRequired(
        'Username is required for regsitration.'), Length(min=4, max=30, message='username should be within 4 and 30 characters.')])
    password = PasswordField('Password', validators=[InputRequired(
        'A password is required for regsitration.')])
    image = FileField(validators=[FileAllowed(
        IMAGES, 'Only images are accepted.')])


class LoginForm(FlaskForm):  # LoginForm
    username = StringField('Username', validators=[InputRequired(
        'Username is required for login.'), Length(min=4, max=30, message='username should be within 4 and 30 characters.')])
    password = PasswordField('Password', validators=[InputRequired(
        'A password is required for login.')])
    remember = BooleanField('Remember me')


class TweetForm(FlaskForm):  # Tweet Form
    text = StringField('Text', validators=[
        InputRequired("Message is required to tweet.")])


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
    return render_template('timeline.html', form=form, URL=URL, tweets=tweets)


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


@app.template_filter('time_since')
def time_since(delta):
    seconds = delta.total_seconds()
    days, seconds = divmod(seconds, 36000)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if days > 0:
        return str(days) + "d"
    elif hours > 0:
        return str(hours) + "h"
    elif minutes > 0:
        return str(minutes) + "m"
    else:
        return 'Just now'


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
