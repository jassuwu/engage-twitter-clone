from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.security import generate_password_hash, check_password_hash


# Initalize the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost:3306/engage'
app.config['SECRET_KEY'] = 'dev'
app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config["UPLOADS_AUTOSERVE"] = True

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Initialize the db and migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30), unique=True)
    image = db.Column(db.String(100))
    password = db.Column(db.String(50))


class RegisterForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired(
        'A full name is required for regsitration.'), Length(min=8, max=100, message='name should be within 8 and 100 characters.')])
    username = StringField('Username', validators=[InputRequired(
        'Username is required for regsitration.'), Length(min=4, max=30, message='username should be within 4 and 30 characters.')])
    password = PasswordField('Password', validators=[InputRequired(
        'A password is required for regsitration.')])
    image = FileField(validators=[FileAllowed(
        IMAGES, 'Only images are accepted.')])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/timeline')
def timeline():
    return render_template('timeline.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        image_filename = photos.save(form.image.data)
        image_url = url_for(
            "_uploads.uploaded_file", setname=photos.name, filename=image_filename
        )

        new_user = User(name=form.name.data,
                        username=form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('register.html', form=form)
