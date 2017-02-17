from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, Blueprint, flash
from flask_login import login_required, logout_user, current_user, login_user

from ..models import User, Student, Teacher, Task
from ..forms import *
from ..pyscripts.question_dict import QUESTIONS

from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
from flask_mail import Message
from app import app,db,mail

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
                #only students have to register
                u = Student(regform.fname.data.lower(), regform.lname.data.lower(), regform.email.data.lower(), regform.password.data, 'student')

                db.session.add(u)
                db.session.commit()

                subject = "Email Confirmation"

                token = serializer.dumps(u.email, salt='email-confirm-key')

                confirm_url = url_for('user.confirm_email',token=token,_external=True)
                html = render_template('emails/confirm_email.html', confirm_url=confirm_url)
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
        recover_url = url_for('user.reset_with_token',token=token,_external=True)
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
        return redirect(url_for('user.login'))
    return render_template('user/reset_with_token.html',form=form,token=token)

@user.route('/account',methods=['GET','POST'])
@login_required
def account():
    #if user.role == 'student': ... LinkForm()
    #if user.role == 'teacher': ... query and show students
    user_id = current_user.user_id
    u = User.query.get(user_id)
    if u.role == 'student':
        changeform = ChangeDetailsForm(obj=u)
        linkform = TeacherLinkForm()
        pwform = ChangePasswordForm1()
        if linkform.link_submit.data and linkform.validate_on_submit():
            t = Teacher.query.filter_by(code=linkform.link_code.data).first()
            if t:
                #create link in association table, Association()?
                s = Student.query.filter_by(user_id=user_id).first()
                a = t.add_student(s)
                if not a:
                    flash('Already linked to this teacher')
                    return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
                db.session.add(a)
                db.session.commit()
                flash('Successfully linked')
                return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
            else:
                flash('No teacher with that code')
                return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
        if changeform.change_submit.data and changeform.validate_on_submit():
            if u.check_pw(changeform.password.data):
                u.fname = changeform.fname.data
                u.lname = changeform.lname.data
                u.email = changeform.email.data
                db.session.add(u)
                db.session.commit()
                flash('Details changed successfully')
                return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
            else:
                flash('Incorrect password')
                return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
        if pwform.pw_submit.data and pwform.validate_on_submit():
            if u.check_pw(pwform.old_password.data):
                u.password = generate_password_hash(pwform.password.data)
                db.session.add(u)
                db.session.commit()
                flash('Password changed successfully')
                return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
            else:
                flash('Incorrect password')
                return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
        return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
    elif u.role == 'teacher':
        students = u.students.all()
        choices = [(s.student_id,s.fname+' '+s.lname) for s in students]
        setform = SetTaskForm(choices)
        changeform = ChangeDetailsForm(obj=u)
        pwform = ChangePasswordForm1()
        if setform.set_submit.data and setform.validate_on_submit():
            t = Teacher.query.filter_by(user_id=user_id).first()
            teach_id = t.teacher_id
            for s_id in setform.student_select.data:
                for q_id in setform.task_select.data:
                    t=Task(q_id,s_id,teach_id)
                    db.session.add(t)
            db.session.commit()
            flash('Tasks set successfully')
            return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
        if changeform.change_submit.data and changeform.validate_on_submit():
            if u.check_pw(changeform.password.data):
                u.fname = changeform.fname.data
                u.lname = changeform.lname.data
                u.email = changeform.email.data
                db.session.add(u)
                db.session.commit()
                flash('Details changed successfully')
                return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
            else:
                flash('Incorrect password')
                return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
        if pwform.pw_submit.data and pwform.validate_on_submit():
            if u.check_pw(pwform.old_password.data):
                u.password = generate_password_hash(pwform.password.data)
                db.session.add(u)
                db.session.commit()
                flash('Password changed successfully')
                return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
            else:
                flash('Incorrect password')
                return render_template('user/student_account.html', student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
        return render_template('user/teacher_account.html', teacher=u, students=students, setform=setform, qs=QUESTIONS, pwform=pwform, changeform=changeform)
    else:
        return abort(500)
