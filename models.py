# thisProject imports
from app import db

# Flask imports
from flask_login import LoginManager, UserMixin


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
