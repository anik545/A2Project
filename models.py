import sqlite3 as sql

def insertUser(Fname,Lname,email,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (Fname,Lname,email,password) VALUES (?,?,?,?)", (Fname,Lname,email,password))
    con.commit()
    con.close()

def retrieveUsers():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT Fname,Lname,email,password FROM users")
    users = cur.fetchall()
    con.close()
    return users

def checkEmailExists(email):
    con = sql.connect("database.db")
    cur = con. cursor()
    cur.execute("SELECT * FROM users WHERE email = '%s'" % (email))
    print(cur.fetchall())
    if cur.fetchone():
        con.close()
        return True
    else:
        con.close()
        return False  #return false if email doesnt exist

def checkLogin(email,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email = '%s' AND password = '%s'" % (email,password))
    if cur.fetchone():
        con.close()
        return True
    else:
        con.close()
        return False
