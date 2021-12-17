from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
    login_manager
)

import logging
logging.basicConfig(filename='logs.log', level=logging.DEBUG,  format='%(levelname)s:%(name)s:%(asctime)s:%(message)s')

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'info'
migrate = Migrate(app, db, render_as_batch=True)
from app import views, models
