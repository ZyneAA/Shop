import os
from werkzeug.security import generate_password_hash
import sqlite3
from flask import redirect, session
from functools import wraps

connection = sqlite3.connect("shop.db", check_same_thread = False)
db = connection.cursor()

#Create account
def acc_creator(name:str, password:str):
    a = (1, name, password, generate_password_hash(password))
    if name != None and password != None:
        db.execute("INSERT INTO users VALUES (?, ?, ?, ?)", a)
        connection.commit()
        db.close()

#View the user
def view(name:str):
    info = []
    db.execute("SELECT * FROM users WHERE name = ?", (name,))
    lol = db.fetchall()
    if lol == []:
        return None
    for i in lol[0]:
        info.append(i)
    return info

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

print(view("zyne"))