from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
import os

# Initialization of various settings necessary for running the application
# See the README.md file
DB_USER = os.getenv('EUREKA_DB_USER')
DB_PASSWORD = os.environ.get('EUREKA_DB_PASSWORD')
DB_NAME = os.environ.get('EUREKA_DB_NAME')
app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@127.0.0.1/{}' \
    .format(DB_USER, DB_PASSWORD, DB_NAME)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
mail = Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
