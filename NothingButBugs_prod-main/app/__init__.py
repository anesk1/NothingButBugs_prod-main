from flask import Flask

# New imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
import os

# force loading of environment variables
load_dotenv('.flaskenv')

# Get the environment variables from .flaskenv
PASSWORD = os.environ.get('DATABASE_PASSWORD')
USERNAME = os.environ.get('DATABASE_USERNAME')
DB_NAME = os.environ.get('DATABASE_NAME')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csc330 spring 2021'

# Add DB config
app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://'
                                        + USERNAME
                                        + ':'
                                        + PASSWORD
                                        + '@db4free.net/'
                                        + DB_NAME)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True


# Create database connection and associate it with the Flask application
db = SQLAlchemy(app)

# Initialize Bootstrap object
bootstrap = Bootstrap(app)

login = LoginManager(app)

# enables @login_required
login.login_view = 'login'

# Add models
from app import routes, models

# Creates DB schema
db.create_all()
