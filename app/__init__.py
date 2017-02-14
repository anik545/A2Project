from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


from flask_mail import Mail

app = Flask(__name__)

app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

mail = Mail(app)

from .routes.matrix import matrix_blueprint
from .routes.questions import questions_blueprint
from .routes.loci import loci_blueprint
from .routes.user import user

app.register_blueprint(matrix_blueprint)
app.register_blueprint(loci_blueprint)
app.register_blueprint(questions_blueprint)
app.register_blueprint(user)


from app import models, views
