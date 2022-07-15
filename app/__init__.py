from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
# login.login_messqge = 'Please login to access this page'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes