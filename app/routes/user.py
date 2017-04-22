from flask import (Blueprint, Flask, abort, flash, jsonify, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash

from app import app, db, mail

from ..forms import (ChangeDetailsForm, ChangePasswordForm,
                     ChangePasswordForm1, LoginForm, RegisterForm,
                     RequestPasswordChangeForm, SetTaskForm, TeacherLinkForm)
from ..models import Student, Task, Teacher, User, Graph
from ..pyscripts.question_dict import QUESTIONS

# Initialise blueprint
user = Blueprint('user', __name__, template_folder='templates')

# Create serializer object -- used to create tokens for emails
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def send_email(address, subject, html):
    """Sends email to address given the html content of email."""
    msg = Message(subject, sender="testapp545545@gmail.com",
                  recipients=[address])
    msg.html = html
    mail.send(msg)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # already logged in user shouldnt go to login page
        return redirect(url_for('main'))
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data.lower()).first()
        # If user exists and password enters is valid
        if user and user.check_pw(loginform.password.data):
            # Login user and update database
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            # Go back to home page
            return redirect(url_for('main'))
        else:
            flash('Incorrect Credentials')
    # Return empty login page if no form submitted or errors on form validation
    return render_template('user/login.html', loginform=loginform)


@user.route('/logout')
@login_required
def logout():
    # Load current user
    user = current_user
    # Unauthenicate
    user.authenticated = False
    # Update database
    db.session.add(user)
    db.session.commit()
    # Log out user and return to home page
    logout_user()
    return redirect(url_for('main'))


@user.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # Already logged in user shouldnt go to register page
        return redirect(url_for('main'))
    regform = RegisterForm()
    if regform.validate_on_submit():
        if not User.query.filter_by(email=regform.email.data.lower()).first():
            # Only students have to register
            # So create student object with form data
            u = Student(regform.fname.data.lower(), regform.lname.data.lower(),
                        regform.email.data.lower(), regform.password.data,
                        'student')
            # Add student object to database.
            db.session.add(u)
            db.session.commit()

            subject = "Email Confirmation"
            #Create token for confimation link
            token = serializer.dumps(u.email, salt='email-confirm-key')
            # Create confirmation url from token
            confirm_url = url_for('user.confirm_email', token=token, _external=True)
            # Render and send confirmation email
            html = render_template('emails/confirm_email.html', confirm_url=confirm_url)
            send_email(address=u.email, subject=subject, html=html)
            # Log in the user and redirect to homepage
            login_user(u)
            flash("Confirmation Email Sent")
            return redirect(url_for('main'))
        else:
            # Cant have two users with the same email
            flash('Email already exists')
    # Return signup page if GET request (no form submitted)
    return render_template('user/signup.html', regform=regform)

@user.route('/confirm/<token>')
def confirm_email(token):
    try:
        # Try to decode the token in the url with the given salt
        # Reject if token is more than an hour old
        # The token decodes to the user's email address
        email = serializer.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        # If the token is invalid and an error is thrown, return 404 error code
        abort(404)
    # Get User from database based on email (from decoded token)
    user = User.query.filter_by(email=email).first_or_404()
    # Set confirmed status
    user.confirmed = True
    # Update database
    db.session.add(user)
    db.session.commit()
    #Log in user and redirect to home page
    login_user(user)
    flash('Email Confirmed')
    return redirect(url_for('main'))


@user.route('/reset', methods=['GET', 'POST'])
def reset():
    #Load form
    form = RequestPasswordChangeForm()
    if form.validate_on_submit():
        #Get user from input email
        user = User.query.filter_by(email=form.email.data).first()
        # If there is no user, display error message and return to same page
        if not user:
            flash('Email address does not exist')
            return render_template('user/reset.html', form=form)
        # If user not confirmed, display error message and return to same page
        elif not user.confirmed:
            flash('Email address not confirmed')
            return render_template('user/reset.html', form=form)
        # If there is a user with that email address, create email
        subject = "Password Reset"
        # Create token based on users email
        token = serializer.dumps(user.email, salt='recover-key')
        # Generate url with the token
        recover_url = url_for('user.reset_with_token', token=token, _external=True)
        # Render and send the email
        html = render_template('emails/recover_email.html', recover_url=recover_url)
        send_email(address=user.email, subject=subject, html=html)
        # Display success message and redirect to home page
        flash('Password reset email sent')
        return redirect(url_for('main'))
    return render_template('user/reset.html', form=form)


@user.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        # Try to decode the token in the url with the given salt
        # Reject if token is more than an hour old
        # The token decodes to the user's email address
        email = serializer.loads(token, salt='recover-key', max_age=86400)
    except:
        # If the token is invalid and an error is thrown, return 404 error code
        abort(404)
    # Load form
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Get User from database based on email (from decoded token)
        user = User.query.filter_by(email=email).first_or_404()
        print(user)
        # Change user's password
        user.password = generate_password_hash(form.password.data)
        # Add updated user to database
        db.session.add(user)
        db.session.commit()
        flash("password updated successfully")
        # Redirect to login page so user logs in with new password
        return redirect(url_for('user.login'))
    return render_template('user/reset_with_token.html', form=form, token=token)


@user.route('/_delete_teacher', methods=['POST'])
def delete_teacher():
    # Get user id
    user_id = current_user.user_id
    # Get student from user_id
    s = Student.query.filter_by(user_id=user_id).first()
    # Get teacher id to be deleted from student and delete link
    teacher_id = request.form.get('teacher_id', None)
    t = Teacher.query.filter_by(teacher_id=teacher_id).first()
    a = t.remove_student(s)
    db.session.add(a)
    db.session.commit()
    return jsonify()  # return nothing (no error)


@user.route('/_delete_student', methods=['POST'])
def delete_student():
    # Get user id
    user_id = current_user.user_id
    # Get teacher from user_id
    t = Teacher.query.filter_by(user_id=user_id).first()
    # Get student id to be deleted from teacher and delete link
    student_id = request.form.get('student_id', None)
    s = Student.query.filter_by(student_id=student_id).first()
    a = t.remove_student(s)
    db.session.add(a)
    db.session.commit()
    return jsonify()  # return nothing (no error)


@user.route('/_delete_graph', methods=['POST'])
def delete_graph():
    # Get id of graph to be deleted
    graph_id = request.form.get('graph_id', None)
    # Query database and delete graph
    g = Graph.query.filter_by(graph_id=graph_id).delete()
    db.session.commit()
    return jsonify()  # return nothing (no error)


@user.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # Get current user data
    user_id = current_user.user_id
    u = User.query.get(user_id)
    if u.role == 'student':
        # Load all forms
        changeform = ChangeDetailsForm(obj=u)
        linkform = TeacherLinkForm()
        pwform = ChangePasswordForm1()
        if linkform.link_submit.data and linkform.validate_on_submit():
            # If the links form is submitted, try to get the teacher with input code
            t = Teacher.query.filter_by(code=linkform.link_code.data).first()
            if t:
                # If teacher with link exists
                # Load student object
                s = Student.query.filter_by(user_id=user_id).first()
                # Try to add this student to the teacher
                a = t.add_student(s)
                if not a:
                    # If add_student returns none, then student is already linked
                    flash('Already linked to this teacher')
                    # Go back to account page
                    return render_template('user/student_account.html',
                        student=u, qs=QUESTIONS, linkform=linkform, changeform=changeform, pwform=pwform)
                # If student not already linked, commit link to database
                db.session.add(a)
                db.session.commit()
                flash('Successfully linked')
                # Go back to account page
                return render_template('user/student_account.html',
                    student=u, qs=QUESTIONS, linkform=linkform,
                    changeform=changeform, pwform=pwform)
            else:
                flash('No teacher with that code')
                # Go back to account page with appropriate message
                return render_template('user/student_account.html',
                    student=u, qs=QUESTIONS, linkform=linkform,
                    changeform=changeform, pwform=pwform)
        if changeform.change_submit.data and changeform.validate_on_submit():
            # If user is changing details, check password is correct
            if u.check_pw(changeform.password.data):
                # Get data from form and change attributes for user
                u.fname = changeform.fname.data
                u.lname = changeform.lname.data
                u.email = changeform.email.data
                # Update user in database.
                db.session.add(u)
                db.session.commit()
                flash('Details changed successfully')
                # Go back to account page with message
                return render_template('user/student_account.html',
                    student=u, qs=QUESTIONS, linkform=linkform,
                    changeform=changeform, pwform=pwform)
            else:
                flash('Incorrect password')
                # Go back to account page with message
                return render_template('user/student_account.html',
                    student=u, qs=QUESTIONS, linkform=linkform,
                    changeform=changeform, pwform=pwform)
        if pwform.pw_submit.data and pwform.validate_on_submit():
            # Make sure old password was input correctly
            if u.check_pw(pwform.old_password.data):
                # Get form data and update users password
                u.password = generate_password_hash(pwform.password.data)
                # Update user in database
                db.session.add(u)
                db.session.commit()
                flash('Password changed successfully')
                # Go back to account page with message
                return render_template('user/student_account.html',
                    student=u, qs=QUESTIONS, linkform=linkform,
                    changeform=changeform, pwform=pwform)
            else:
                flash('Incorrect password')
                # Go back to account page with message
                return render_template('user/student_account.html',
                    student=u, qs=QUESTIONS, linkform=linkform,
                    changeform=changeform, pwform=pwform)
        return render_template('user/student_account.html', student=u,
                                qs=QUESTIONS, linkform=linkform,
                                changeform=changeform, pwform=pwform)
    elif u.role == 'teacher':
        # Get all the teachers linked students from the database
        students = u.students.all()
        # List of tuples (student_id,student_name) for each student
        # Used in SetForm, when a teacher chooses which students to set which tasks
        choices = [(s.student_id, s.fname+' '+s.lname) for s in students]
        # Load forms
        setform = SetTaskForm(choices)
        changeform = ChangeDetailsForm(obj=u)
        pwform = ChangePasswordForm1()
        if setform.set_submit.data and setform.validate_on_submit():
            # If setform submitted (form for setting tasks)
            # Get teacher object from user_id
            t = Teacher.query.filter_by(user_id=user_id).first()
            teach_id = t.teacher_id
            # Loop over each student selected
            for s_id in setform.student_select.data:
                # Loop over each tasks selected
                for q_id in setform.task_select.data:
                    # Set task to student
                    t = Task(q_id, s_id, teach_id)
                    # Add to database
                    db.session.add(t)
            # Commit database changes
            db.session.commit()
            # Go back to account page with success message
            flash('Tasks set successfully')
            return render_template('user/teacher_account.html', teacher=u, students=students, setform=setform, qs=QUESTIONS, pwform=pwform, changeform=changeform)
        if changeform.change_submit.data and changeform.validate_on_submit():
            if u.check_pw(changeform.password.data):
                # Get data from form and change attributes for user
                u.fname = changeform.fname.data
                u.lname = changeform.lname.data
                u.email = changeform.email.data
                # Update user in database
                db.session.add(u)
                db.session.commit()
                # Go back to account page with message
                flash('Details changed successfully')
                return render_template('user/teacher_account.html',
                    teacher=u, students=students, setform=setform,
                    qs=QUESTIONS, pwform=pwform, changeform=changeform)
            else:
                flash('Incorrect password')
                return render_template('user/teacher_account.html',
                    teacher=u, students=students, setform=setform,
                    qs=QUESTIONS, pwform=pwform, changeform=changeform)
        if pwform.pw_submit.data and pwform.validate_on_submit():
            if u.check_pw(pwform.old_password.data):
                # Get form data and update users password
                u.password = generate_password_hash(pwform.password.data)
                db.session.add(u)
                db.session.commit()
                # Go back to account page with success message
                flash('Password changed successfully')
                return render_template('user/teacher_account.html',
                    teacher=u, students=students, setform=setform,
                    qs=QUESTIONS, pwform=pwform, changeform=changeform)
            else:
                # Go back to account page with error message
                flash('Incorrect password')
                return render_template('user/teacher_account.html',
                    teacher=u, students=students, setform=setform,
                    qs=QUESTIONS, pwform=pwform, changeform=changeform)
        return render_template('user/teacher_account.html',
            teacher=u, students=students, setform=setform, qs=QUESTIONS,
            pwform=pwform, changeform=changeform)
    else:
        return abort(500)
