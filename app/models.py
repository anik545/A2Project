from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    user_id = db.Column('user_id',db.Integer, primary_key=True)
    fname = db.Column(db.String(80), unique=False)
    lname = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=False)
    authenticated = db.Column(db.Boolean,default=False)
    confirmed = db.Column(db.Boolean)
    marks = db.relationship('Mark',backref="user",cascade="all, delete-orphan", lazy="dynamic")
    graphs = db.relationship('Graph',backref="user",cascade="all, delete-orphan", lazy="dynamic")

    def __init__(self,fname,lname,email,password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = generate_password_hash(password)
        self.authenticated = False
        self.confirmed = False

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

#teacher class subclassing from user, teacher code field extra
#links table, many to many intermediate, teacher_id, student_id.

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
