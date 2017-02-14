from flask_wtf import Form,FlaskForm
from wtforms import TextField,PasswordField,BooleanField,validators
from wtforms.fields.html5 import EmailField

class RegisterForm(FlaskForm):
    fname = TextField('First Name',[validators.Required()])
    lname = TextField('Last Name',[validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    confirm_password = PasswordField('Confirm Password',[validators.Required(),validators.EqualTo('password',message='Passwords do not match')])
    email=EmailField('Email Address',[validators.DataRequired(),validators.Email()])

class LoginForm(FlaskForm):
    email = TextField('Username',[validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    remember = BooleanField('Remember')

class RequestPasswordChangeForm(FlaskForm):
    email = TextField('Email', [validators.Required(),validators.Email()])

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', [validators.Required()])
    confirm_password = PasswordField('Confirm', [validators.Required(),validators.EqualTo('password',message='Passwords do not match')])
