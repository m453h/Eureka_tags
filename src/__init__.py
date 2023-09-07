from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

DB_USER = os.getenv('EUREKA_DB_USER')
DB_PASSWORD = os.environ.get('EUREKA_DB_PASSWORD')
DB_NAME = os.environ.get('EUREKA_DB_NAME')
app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'Change this for security'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@127.0.0.1/{}'.format(DB_USER, DB_PASSWORD, DB_NAME)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
