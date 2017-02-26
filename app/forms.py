from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, SelectMultipleField,
                     SubmitField, TextField, validators, widgets)
from wtforms.fields.html5 import EmailField

from .pyscripts.question_dict import QUESTIONS


class RegisterForm(FlaskForm):
    """Form to register a new user (student only)"""

    fname = TextField('First Name', [validators.Required()])
    lname = TextField('Last Name', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    confirm_password = PasswordField('Confirm Password', [validators.Required(
    ), validators.EqualTo('password', message='Passwords do not match')])
    email = EmailField('Email Address', [
                       validators.DataRequired(), validators.Email()])


class LoginForm(FlaskForm):
    """Form for a user to log in"""

    email = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    remember = BooleanField('Remember')


class RequestPasswordChangeForm(FlaskForm):
    """Form to request password change email to be sent"""

    email = TextField('Email', [validators.Required(), validators.Email()])


class ChangePasswordForm(FlaskForm):
    """Form for changing password (coming from email)"""

    password = PasswordField('Password', [validators.Required()])
    confirm_password = PasswordField('Confirm', [validators.Required(
    ), validators.EqualTo('password', message='Passwords do not match')])


class TeacherLinkForm(FlaskForm):
    """Form for students account page to link to teachers"""

    link_code = TextField('Link Code', [validators.Required()])
    link_submit = SubmitField('Go')


class MultiCheckboxField(SelectMultipleField):
    """Field for SetTaskForm (multiple select with checkboxes)"""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SetTaskForm(FlaskForm):
    """Form for teachers account page to set students tasks"""
    student_select = MultiCheckboxField('Students',
                                        [validators.Required()], coerce=int)
    task_select = MultiCheckboxField('Tasks',[validators.Required()], coerce=int, choices=[(q['id'], q['topic'] + '  ' + q['name']) for q in QUESTIONS])
    set_submit = SubmitField('Go')

    def __init__(self, selection_choices):
        """Override init so form can be initialized with custom choices."""
        super(SetTaskForm, self).__init__()
        self.student_select.choices = selection_choices


class ChangeDetailsForm(FlaskForm):
    """Form for teacher and student account page for changing name(s), email."""

    fname = TextField('First Name', [validators.Required()])
    lname = TextField('Last Name', [validators.Required()])
    email = EmailField('Email Address',
                       [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.Required()])
    change_submit = SubmitField('Go')


class ChangePasswordForm1(FlaskForm):
    """Form for changing password from account page."""

    old_password = PasswordField('Old Password', [validators.Required()])
    password = PasswordField('New Password', [validators.Required()])
    confirm_password = PasswordField('Confirm New Password', [validators.Required(), validators.EqualTo('password', message='Passwords do not match')])
    pw_submit = SubmitField('Go')
