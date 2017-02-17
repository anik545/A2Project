from app import db
from app.models import *

db.create_all()
u1=Student('John','Smith','a@b.com','abc','student')
u2=Student('Bob','Ross','a@C.com','abc1','student')
u3=Student('Alex','Smith','a@D.com','abc12','student')
u4=Student('Dan','Jones','a@e.com','abc123','student')
u5=Student('Mike','Red','a@f.com','abc1234','student')
u6=Student('Jack','Deer','a@g.com','1','student')
u7=Student('George','Russel','a@h.com','12','student')
u8=Student('Harvey','Miller','a@i.com','123','student')
u9=Student('Albert','Parker','a@j.com','1234','student')
u10=Student('Mary','Cole','a@k.com','12345','student')
u11=Student('Anik','Roy','anik545@gmail.com','January28','student')

t1=Teacher('Stephen','Jackson','a@x.com','cde','teacher')
t2=Teacher('Laura','Morris','a@y.com','def','teacher')


db.session.add_all([u1,u2,u3,u4,u5,u6,u7,u8,u9,u10,u11,t1,t2])
db.session.commit()

a,b,c,x,y = t1.add_student(u11), t1.add_student(u10), t1.add_student(u9), t1.add_student(u8), t1.add_student(u7)

d,e,f,g,h,i,j = t2.add_student(u1), t2.add_student(u2), t2.add_student(u3), t2.add_student(u4), t2.add_student(u5), t2.add_student(u9), t2.add_student(u10)

db.session.add_all([a,b,c,d,e,f,g,h,i,j,x,y])

db.session.commit()
