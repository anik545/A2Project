import sqlite3 as sql
from os import path

ROOT = path.dirname(path.realpath(__file__))

def insertUser(Fname,Lname,email,password):
    con = sql.connect(path.join(ROOT, "database.db"))
    cur = con.cursor()
    cur.execute("INSERT INTO users (Fname,Lname,email,password) VALUES (?,?,?,?)", (Fname,Lname,email,password))
    con.commit()
    con.close()

def retrieveUsers():
    con = sql.connect(path.join(ROOT, "database.db"))
    cur = con.cursor()
    cur.execute("SELECT Fname,Lname,email,password FROM users")
    users = cur.fetchall()
    con.close()
    return users

def checkEmailExists(email):
    con = sql.connect(path.join(ROOT, "database.db"))
    cur = con. cursor()
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())
    cur.execute("SELECT * FROM users WHERE email = '%s'" % (email))
    print(cur.fetchall())
    if cur.fetchone():
        con.close()
        return True
    else:
        con.close()
        return False  #return false if email doesnt exist

def checkLogin(email,password):
    con = sql.connect(path.join(ROOT, "database.db"))
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email = '%s' AND password = '%s'" % (email,password))
    if cur.fetchone():
        con.close()
        return True
    else:
        con.close()
        return False
