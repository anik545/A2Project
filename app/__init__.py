from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


from flask_mail import Mail

# Create app and initialize flask
app = Flask(__name__)

#load configuration options from config.py
app.config.from_object('config')

# Initialize flask-login and set up login manage
login_manager = LoginManager()
login_manager.init_app(app)
# The view which flask login redirects to if user is not logged in and trys to access restricted view
login_manager.login_view = 'user.login'

# Initialize database with sqlalchemy
db = SQLAlchemy(app)

# Initialize flask-mail
mail = Mail(app)

# Import and register all blueprints
from .routes.matrix import matrix_blueprint
from .routes.questions import questions_blueprint
from .routes.loci import loci_blueprint
from .routes.user import user

# Blueprints used to break up larger app into smaller modules
app.register_blueprint(matrix_blueprint)
app.register_blueprint(loci_blueprint)
app.register_blueprint(questions_blueprint)
app.register_blueprint(user)

# Import all other views and database models
from app import models, views
