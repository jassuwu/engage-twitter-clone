# Flask imports
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

# Non-flask imports
from wtforms import StringField, IntegerField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length


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
