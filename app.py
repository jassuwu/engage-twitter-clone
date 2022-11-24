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


# Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.template_filter('time_since')  # Template filter for time_since tweet
def time_since(delta):
    seconds = delta.total_seconds()
    days, seconds = divmod(seconds, 36000)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if days > 0:
        return str(int(days)) + "d"
    elif hours > 0:
        return str(int(hours)) + "h"
    elif minutes > 0:
        return str(int(minutes)) + "m"
    else:
        return 'Just now'


# Views import
from views import *
