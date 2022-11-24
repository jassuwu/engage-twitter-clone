# thisProject imports
from app import db

# Flask imports
from flask_login import LoginManager, UserMixin


# The relationship table
followers = db.Table('follower',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followee_id', db.Integer, db.ForeignKey('user.id')))


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
    # 4. added following backref when adding the follower model
    following = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followee_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )
    # 5. added after the prev backref
    followed_by = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.followee_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        backref=db.backref('followees', lazy='dynamic'),
        lazy='dynamic'
    )


class Tweet(db.Model):  # Tweet Model
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.Text)
    date_created = db.Column(db.DateTime)
