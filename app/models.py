from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

class User(db.Model):
    user_id = db.Column('user_id',db.Integer, primary_key=True)
    fname = db.Column(db.String(80), unique=False)
    lname = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=False)
    authenticated = db.Column(db.Boolean,default=False)
    confirmed = db.Column(db.Boolean)
    role = db.Column(db.String(50))
    graphs = db.relationship('Graph',backref="user",cascade="all, delete-orphan", lazy="dynamic")

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':role
    }

    def __init__(self,fname,lname,email,password,role,auth=False,conf=False):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.role = role
        self.password = generate_password_hash(password)
        self.authenticated = auth
        self.confirmed = conf

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

#http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#using-relationships-with-inheritance
class Teacher(User):
    __tablename__ = 'teacher'
    teacher_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    code = db.Column(db.String(7))
    students = db.relationship('Student', secondary = 'links',backref=db.backref('teachers',lazy='dynamic'),lazy='dynamic')
    tasks = db.relationship('Task',backref="teacher",cascade="all, delete-orphan", lazy="dynamic")
    #could also be just one id field

    def add_student(self, student):
        if not self.has_student(student):
            self.students.append(student)
            return self

    def remove_student(self, student):
        if self.has_student(student):
            self.students.remove(student)
            return self

    def has_student(self, student):
        return self.students.filter(links.c.student_id == student.student_id).count() > 0

    def __init__(self,fname,lname,email,password,role):
        super().__init__(fname,lname,email,password,role)
        self.code=''.join(random.choice(string.ascii_letters) for x in range(7))

    __mapper_args__ = {
        'polymorphic_identity':'teacher',
    }

class Student(User):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    marks = db.relationship('Mark',backref="student",cascade="all, delete-orphan", lazy="dynamic")
    tasks = db.relationship('Task',backref="student",cascade="all, delete-orphan", lazy="dynamic")

    #could also be just one id field
    #TODO only students can have marks, so that relationship can go here.

    __mapper_args__ = {
        'polymorphic_identity':'student',
    }

links = db.Table('links',
    db.Column('teacher_id',db.Integer,db.ForeignKey('teacher.teacher_id')),
    db.Column('student_id',db.Integer,db.ForeignKey('student.student_id'))
)

class Mark(db.Model):
    mark_id = db.Column('mark_id',db.Integer,primary_key=True)
    score = db.Column(db.Integer)
    out_of = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    question_id = db.Column(db.Integer)
    student_id = db.Column('student_id', db.Integer, db.ForeignKey('student.student_id'))
    task = db.relationship('Task',uselist=False, back_populates='mark')

    #TODO make it so only student has marks

    def __init__(self,score,out_of,q_id,student_id):
        self.score=score
        self.out_of = out_of
        self.question_id = q_id
        self.student_id = student_id
        self.date = datetime.date.today()

    def complete_task():
        #add to task
        pass

class Task(db.Model):
    task_id = db.Column('task_id',db.Integer,primary_key=True)
    completed = db.Column(db.Boolean)
    question_id = db.Column(db.Integer)
    student_id = db.Column('student_id', db.Integer, db.ForeignKey('student.student_id'))
    teacher_id = db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.teacher_id'))
    mark_id = db.Column('mark_id', db.Integer, db.ForeignKey('mark.mark_id'))
    mark = db.relationship('Mark', back_populates='task')

    def __init__(self,q_id,student_id,teacher_id):
        self.question_id = q_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.completed = False

    def add_mark(self):
        #add mark only if mark doesnt already exist
        pass

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
