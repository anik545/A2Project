from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, Blueprint
from flask_login import login_required, logout_user, current_user, login_user

from ..models import User
from ..forms import RegisterForm, LoginForm, RequestPasswordChangeForm, ChangePasswordForm
from ..pyscripts.question_dict import QUESTIONS

from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import app,db

user = Blueprint('user',__name__,template_folder='templates')

serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

def send_email(address,subject,html):
    msg=Message(subject,sender="testapp545545@gmail.com",recipients=[address])
    msg.html = html
    mail.send(msg)

@user.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))  #already logged in user shouldnt go to login page
    if request.method == 'GET':
        loginform = LoginForm()
    if request.method == 'POST':
        loginform = LoginForm(request.form)
        if loginform.validate():
            user = User.query.filter_by(email=loginform.email.data.lower()).first()
            if user and user.check_pw(loginform.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('main')) #TODO redirect to last page
            else:
                flash('Incorrect Credentials')
    return render_template('user/login.html',loginform=loginform)

@user.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template('index.html')


@user.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    if request.method == 'GET':
        regform = RegisterForm()
    if request.method == 'POST':
        regform = RegisterForm(request.form)
        if regform.validate():
            if not User.query.filter_by(email=regform.email.data.lower()).first():
                u = User(regform.fname.data.lower(),regform.lname.data.lower(),regform.email.data.lower(),regform.password.data)
                db.session.add(u)
                db.session.commit()

                subject = "Email Confirmation"

                token = serializer.dumps(u.email, salt='email-confirm-key')

                confirm_url = url_for('confirm_email',token=token,_external=True)
                html = render_template('emails/confirm_email.html',confirm_url=confirm_url)
                send_email(address=u.email,subject=subject,html=html)

                login_user(u)
                flash("Confirmation Email Sent")
                return redirect(url_for('main'))
            else:
                flash('Email already exists')
        else:
            error = 'Incorrect Details'
    return render_template('user/signup.html',regform=regform)

@user.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt="email-confirm-key",max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()
    user.confirmed = True

    login_user(user)

    db.session.add(user)
    db.session.commit()

    flash('Email Confirmed')
    return redirect(url_for('main'))

@user.route('/reset',methods=['GET','POST'])
def reset():
    form = RequestPasswordChangeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash('Email address does not exist')
            return render_template('user/reset.html',form=form)
        elif not user.confirmed:
            flash('Email address not confirmed')
            return render_template('user/reset.html',form=form)


        subject = "Password Reset"
        token = serializer.dumps(user.email,salt='recover-key')
        recover_url = url_for('reset_with_token',token=token,_external=True)
        html = render_template('emails/recover_email.html',recover_url=recover_url)

        send_email(address=user.email,subject=subject,html=html)
        flash('Password reset email sent')
        return redirect(url_for('main'))
    return render_template('user/reset.html',form=form)

@user.route('/reset/<token>',methods=['GET','POST'])
def reset_with_token(token):
    try:
        email = serializer.loads(token,salt='recover-key',max_age=86400)
    except:
        abort(404)
    form=ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()
        user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("password updated successfully")
        return redirect(url_for('login'))
    return render_template('user/reset_with_token.html',form=form,token=token)


@user.route('/account')
@login_required
def account():
    user_id = current_user.user_id
    u = User.query.get(user_id)
    return render_template('user/account.html',user=u,qs=QUESTIONS)
