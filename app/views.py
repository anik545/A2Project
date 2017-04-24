from flask import render_template

from app import app, login_manager
from app.models import User


@login_manager.user_loader
def user_loader(email):
    """Return user object for Flask-Login."""
    return User.query.filter_by(email=email).first()


@app.route('/')
def main():
    return render_template('index.html')
