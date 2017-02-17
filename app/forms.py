from flask_wtf import Form,FlaskForm
from wtforms import TextField, PasswordField, SelectMultipleField, BooleanField, validators, widgets, SubmitField
from wtforms.fields.html5 import EmailField
from .pyscripts.question_dict import QUESTIONS

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

class TeacherLinkForm(FlaskForm):
    link_code = TextField('Link Code',[validators.Required()])
    link_submit = SubmitField('Go')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SetTaskForm(FlaskForm):
    student_select = MultiCheckboxField('Students', [validators.Required()], coerce=int)
    task_select = MultiCheckboxField('Tasks', [validators.Required()], coerce=int, choices=[(q['id'], q['topic'] + '  ' + q['name']) for q in QUESTIONS])
    set_submit = SubmitField('Go')

    def __init__(self, selection_choices):
        super(SetTaskForm, self).__init__()
        self.student_select.choices = selection_choices

class ChangeDetailsForm(FlaskForm):
    fname = TextField('First Name',[validators.Required()])
    lname = TextField('Last Name',[validators.Required()])
    email = EmailField('Email Address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password',[validators.Required()])
    change_submit = SubmitField('Go')

class ChangePasswordForm1(FlaskForm):
    '''Changing password from account page'''
    old_password = PasswordField('Old Password', [validators.Required()])
    password = PasswordField('New Password', [validators.Required()])
    confirm_password = PasswordField('Confirm New Password', [validators.Required(),validators.EqualTo('password',message='Passwords do not match')])
    pw_submit = SubmitField('Go')

#ChangePasswordForm
