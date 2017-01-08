from flask import Flask, render_template, request, jsonify,  abort, redirect, url_for, g, flash, session
from complex_loci import *
from matrix_questions import MatrixQuestion
from complex_questions import ComplexQuestion

import ast

from views.matrix import matrix_blueprint

from flask_wtf import Form,FlaskForm
from wtforms import TextField,PasswordField,BooleanField,validators
from wtforms.fields.html5 import EmailField

from flask_login import login_required, logout_user, current_user, login_user, LoginManager

from flask_mail import Mail,Message

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

import datetime

from question_dict import COMPLEX_QUESTIONS,MATRIX_QUESTIONS,QUESTIONS

from itsdangerous import URLSafeTimedSerializer

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

app = Flask(__name__)
app.register_blueprint(matrix_blueprint)
app.config["WTF_CSRF_ENABLED"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config["MAIL_PORT"] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'testapp545545'
app.config['MAIL_PASSWORD'] = 'January28'

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

mail = Mail(app)

def send_email(address,subject,html):
    msg=Message(subject,sender="testapp545545@gmail.com",recipients=[address])
    msg.html = html
    mail.send(msg)


class User(db.Model):
    user_id = db.Column('user_id',db.Integer, primary_key=True)
    fname = db.Column(db.String(80), unique=False)
    lname = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=False)
    authenticated = db.Column(db.Boolean,default=False)
    marks = db.relationship('Mark',backref="user",cascade="all, delete-orphan", lazy="dynamic")
    graphs = db.relationship('Graph',backref="user",cascade="all, delete-orphan", lazy="dynamic")

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

class Mark(db.Model):
     key = db.Column('key',db.Integer,primary_key=True)
     score = db.Column(db.Integer)
     out_of = db.Column(db.Integer)
     date = db.Column(db.DateTime)
     question_id = db.Column(db.Integer)
     user_id = db.Column('user_id',db.Integer,db.ForeignKey('user.user_id'))

     def __init__(self,score,out_of,q_id,user_id):
         self.score=score
         self.out_of=out_of
         self.question_id=q_id
         self.user_id = user_id
         self.date = datetime.date.today()

class Graph(db.Model):
    graph_id = db.Column('graph_id',db.Integer,primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String, nullable=True)
    desmosdata = db.Column(db.String)
    exprlist = db.Column(db.String)
    date = db.Column(db.DateTime)
    image_url = db.Column(db.String)
    user_id = db.Column('user_id',db.Integer,db.ForeignKey('user.user_id'))

    def __init__(self,desmosdata,exprlist,user_id,title,desc,image_url):
        self.desmosdata = desmosdata
        self.exprlist = exprlist
        self.user_id = user_id
        self.title = title
        self.description = desc
        self.image_url = image_url
        self.date = datetime.date.today()

# TODO http://librosweb.es/libro/explore_flask/chapter_12/forgot_your_password.html
# TODO add email confirmation

@login_manager.user_loader
def user_loader(email):
    print(email)
    return User.query.filter_by(email=email).first()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/login',methods=['GET','POST'])
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
        regform = RegisterForm()
    if request.method == 'POST':
        regform = RegisterForm(request.form)
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

@app.route('/reset',methods=['GET','POST'])
def reset():
    form = RequestPasswordChangeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        subject = "Password Reset"

        token = ts.dumps(user.email,salt='recover-key')

        recover_url = url_for('reset_with_token',token=token,_external=True)

        html = render_template('recover_email.html',recover_url=recover_url)

        send_email(address=user.email,subject=subject,html=html)
        flash('Password reset email sent')
        return redirect(url_for('main'))
    return render_template('reset.html',form=form)

@app.route('/reset/<token>',methods=['GET','POST'])
def reset_with_token(token):
    try:
        email = ts.loads(token,salt='recover-key',max_age=86400)
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
    return render_template('reset_with_token.html',form=form,token=token)


@app.route('/account')
@login_required
def account():
    user_id = current_user.user_id
    u = User.query.get(user_id)
    return render_template('account.html',user=u,qs=QUESTIONS)

@app.route('/loci-plotter')
def loci():
    if current_user.is_authenticated:
        user = User.query.get(current_user.user_id)
        user_graphs = user.graphs.all()
    else:
        user_graphs = None
    return render_template('loci.html',user_graphs=user_graphs)


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

@app.route('/_addgraph',methods=['GET','POST'])
@login_required
def addgraph():
    if request.method=='POST':
        try:
            data1 = request.form.get('desmosdata',None)
            data2 = request.form.get('exprlist',None)
            title = request.form.get('title',"")
            desc = request.form.get('description',"")
            image_url = request.form.get('image',"")
            user_id = current_user.user_id
            print(type(Graph.query.filter_by(title=title,user_id=user_id).first()))
            exists = Graph.query.filter_by(title=title,user_id=user_id).first()
            if exists:
                return jsonify(status="error",error="Graph already exists")
            else:
                g=Graph(data1,data2,user_id,title,desc,image_url)
                db.session.add(g)
                db.session.commit()
                graph_id = g.graph_id #has to be after commit
                return jsonify(id=graph_id,title=title,image_url=image_url,desc=desc,status="ok",error=None)
        except Exception as e:
            print(e)
            return jsonify(status="error",error="Error saving Graph")
    if request.method=='GET':
        try:
            graph_id = request.args.get('graph_id',None)
            g = Graph.query.get(graph_id)
            return jsonify(desmosdata=g.desmosdata,exprlist=g.exprlist)
        except Exception as e:
            print(e)
            return abort(500)

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
        session['questions'] = [q.get_question() for q in questions]
        session['answers'] = [str(q.get_answer()) for q in questions]
        return render_template('mat_questions.html',questions=enumerate(questions),answers=answers,mat_ans=matans,q_type=q_type,topic=topic)
    elif topic == 'complex':
        questions = [ComplexQuestion(q_type) for x in range(q_number)]
        answers = [q.get_answer() for q in questions]
        session['questions'] = [q.get_question() for q in questions]
        session['answers'] = [str(q.get_answer()) for q in questions]
        return render_template('complex_questions.html',questions=enumerate(questions),answers=answers,q_type=q_type,topic=topic)
    else:
        abort(404)


@app.route('/questions/_answers/<topic>/<q_type>')
def answers(topic,q_type):
    if topic == 'matrix':
        question_id = MATRIX_QUESTIONS[q_type]
        answers = session['answers']
        if q_type == 'det':
            question_id=3
            inputs = [request.form.get(str(x),0) for x in range(10)]
            inputs = [int(x) if x else 0 for x in inputs]
            scores = []
            for n,x in enumerate(answers):
                if x == inputs[n]:
                    scores.append(1)
                else:
                    scores.append(0)
            percent = sum(scores)*100//len(answers)
        else:
            answers = [[[str(i) for i in j] for j in ast.literal_eval(a)] for a in answers]
            inputs=[]
            for n,a in enumerate(answers):
                inputs.append([])
                for x in range(len(a)):
                    inputs[n].append([])
                    for y in range(len(a[0])):
                        i=request.args.get(str(n)+str(x)+str(y),0)
                        if i:
                            inputs[n][x].append(i)
                        else:
                            inputs[n][x].append('0')
            scores = []
            for n,x in enumerate(answers):
                if x == inputs[n]:
                    scores.append(1)
                else:
                    scores.append(0)
            percent = sum(scores)*100//len(answers)
        questions = session['questions']
        answers = [str(a).replace("'","") for a in answers]
        inputs = [str(i).replace("'","") for i in inputs]
        if current_user.is_authenticated:
            mark = Mark(sum(scores),len(scores),question_id,current_user.user_id)
            db.session.add(mark)
            db.session.commit()
        return jsonify(answers=answers,inputs=inputs,questions=questions,percent=percent,scores=scores)

    elif topic == 'complex':
        question_id = COMPLEX_QUESTIONS[q_type]
        answers = session['answers']
        if q_type == 'mod_arg':
            inputs = []
            for x in range(len(answers)):
                inputs.append((request.args.get(str(x)+'mod',0),request.args.get(str(x)+'arg',0)))
            answers = [(str(i),str(j)) for i,j in [ast.literal_eval(a) for a in answers]]
            scores=[]
            for n,x in enumerate(answers):
                if x==inputs[n]:
                    scores.append(1)
                else:
                    scores.append(0)
            percent=sum(scores)*100//len(answers)
            pass
        else:
            inputs = []
            for x in range(10):
                inputs.append(str(request.args.get(str(x)+'re',0))+'+'+str(request.args.get(str(x)+'im',0))+'j')
            scores=[]
            for n,x in enumerate(answers):
                print(x,'||',inputs[n])
                if complex(x) == complex(inputs[n]):
                    scores.append(1)
                else:
                    scores.append(0)
            percent = sum(scores)*100//len(answers)
        questions = session['questions']
        print(scores)
        if current_user.is_authenticated:
            mark = Mark(sum(scores),len(scores),question_id,current_user.user_id)
            db.session.add(mark)
            db.session.commit()
        return jsonify(answers=answers,inputs=inputs,questions=questions,percent=percent,scores=scores)
    else:
        abort(404)


@app.route('/ttt')
def ttt():
    return render_template('ttt.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
