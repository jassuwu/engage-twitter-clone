from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

# Initalize the app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/timeline')
def timeline():
    return render_template('timeline.html')


@app.route('/register')
def register():
    return render_template('register.html')
