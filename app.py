from flask import Flask, render_template, request, jsonify, abort,redirect,url_for,g,flash
from complex_loci import *
from matrix_questions import MatrixQuestion
from complex_questions import ComplexQuestion

import ast

from views.matrix import matrix_blueprint

from flask_wtf import Form,FlaskForm
from wtforms import TextField,PasswordField,BooleanField,validators
from wtforms.fields.html5 import EmailField

from flask_login import login_required, logout_user, current_user, login_user, LoginManager

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

class Register(FlaskForm):
    fname = TextField('First Name',[validators.Required()])
    lname = TextField('Last Name',[validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    confirm_password = PasswordField('Confirm Password',[validators.Required(),validators.EqualTo('password',message='Passwords do not match')])
    email=EmailField('Email Address',[validators.DataRequired(),validators.Email()])

class Login(FlaskForm):
    email = TextField('Username',[validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    remember = BooleanField('Remember')


app = Flask(__name__)
app.register_blueprint(matrix_blueprint)
app.config["WTF_CSRF_ENABLED"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column('user_id',db.Integer, primary_key=True)
    fname = db.Column(db.String(80), unique=False)
    lname = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=False)
    authenticated = db.Column(db.Boolean,default=False)

    def __init__(self,fname,lname,email,password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = generate_password_hash(password)
        self.authenticated = False

    def check_pw(self,password):
        return check_password_hash(self.password,password)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

@login_manager.user_loader
def user_loader(email):
    print(email)
    return User.query.filter_by(email=email).first()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))  #already logged in user shouldnt go to login page
    if request.method == 'GET':
        loginform = Login()
    if request.method == 'POST':
        loginform = Login(request.form)
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
    return render_template('login.html',loginform=loginform)

@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template('index.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    if request.method == 'GET':
        regform = Register()
    if request.method == 'POST':
        regform = Register(request.form)
        if regform.validate():
            if not User.query.filter_by(email=regform.email.data.lower()).first():
                u = User(regform.fname.data.lower(),regform.lname.data.lower(),regform.email.data.lower(),regform.password.data)
                db.session.add(u)
                db.session.commit()
                login_user(u)
                return redirect(url_for('main'))
            else:
                flash('Email already exists')
        else:
            error = 'Incorrect Details'
    return render_template('signup.html',regform=regform)

@app.route('/loci-plotter')
def loci():
    return render_template('loci.html')


@app.route('/_plot')
def plot():
    eq = request.args.get('eq', 0, type=str)
    try:
        line = get_implicit(eq, latx=True)
        print(line)
        if ' i ' in line:
            print('i in line')
            raise TypeError
        print(line)
        return jsonify(result=line)
    except Exception as e:
        print(e)
        abort(500)


@app.route('/operations-argand')
def operations():
    return render_template('operations.html')

@app.route('/questions')
def questions():
    return render_template('questions.html')

@app.route('/questions/<topic>/<q_type>')
def show_questions(topic,q_type):
    q_number = request.args.get('n',10)
    if topic == 'matrix':
        questions = [MatrixQuestion(q_type) for x in range(q_number)]
        answers = [q.get_answer() for q in questions]
        matans=questions[0].mat_ans
        return render_template('mat_questions.html',questions=enumerate(questions),answers=answers,mat_ans=matans)
    elif topic == 'complex':
        questions = [ComplexQuestion(q_type) for x in range(q_number)]
        answers = [q.get_answer() for q in questions]
        return render_template('complex_questions.html',questions=enumerate(questions),answers=answers,q_type=q_type)
    else:
        abort(404)

@app.route('/questions/answers/<topic>',methods=['GET','POST'])
def show_answers(topic):
    if topic == 'matrix':
        answers = request.args.getlist('ans',None)
        mat_ans = request.args.get('mat_ans','True')
        if mat_ans == 'True':
            answers = [[[str(i) for i in j] for j in ast.literal_eval(a)] for a in answers]
            inputs=[]
            for n,a in enumerate(answers):
                inputs.append([])
                for x in range(len(a)):
                    inputs[n].append([])
                    for y in range(len(a[0])):
                        inputs[n][x].append(request.form.get(str(n)+str(x)+str(y),0))
            score = 0
            for n,x in enumerate(answers):
                if x == inputs[n]:
                    score+=1
            percent = score*100//len(answers)

        else:
            inputs = [request.form.get(str(x),0) for x in range(10)]
            inputs = [int(x) if x else 0 for x in inputs]
            score = 0
            for n,x in enumerate(answers):
                if x == inputs[n]:
                    score+=1
            percent = score*100//len(answers)
        print(inputs)
        print(answers)
        return render_template('answers.html',ans=answers,inputs=inputs,percent=percent)

    if topic == 'complex':
        answers = request.args.getlist('ans',None)
        q_type = request.args.get('q_type',None)
        inputs=[]
        if q_type == 'mod_arg':
            for x in range(len(answers)):
                inputs.append((request.form.get(str(x)+'mod',0),request.form.get(str(x)+'arg',0)))
            answers = [(str(i),str(j)) for i,j in [ast.literal_eval(a) for a in answers]]
            score=0
            for n,x in enumerate(answers):
                print(x,inputs[n])
                if x==inputs[n]:
                    score+=1
            percent=score*100//len(answers)
        else:
            for x in range(len(answers)):
                inputs.append(str(request.form.get(str(x)+'re',0))+'+'+str(request.form.get(str(x)+'im',0))+'j')
            score = 0
            for n,x in enumerate(answers):
                print(x,inputs[n])
                if complex(x) == complex(inputs[n]):
                    score +=1
            percent = score*100//len(answers)

        print(inputs)
        print(answers)
        return render_template('answers.html',ans=answers,inputs=inputs,percent=percent)
    else:
        abort(404)


@app.route('/ttt')
def ttt():
    return render_template('ttt.html')

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
