import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from _vnh import view, login_required
from datetime import datetime


app = Flask(__name__)
app.secret_key = "good"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/home")
@login_required
def home():
    return render_template("home.html")
    
@app.route("/buys")
@login_required
def buys():
    return render_template("buys.html")

@app.route("/sales")
@login_required
def sales():
    return render_template("sales.html")

@app.route("/graphs")
@login_required
def graphs():
    return render_template("graphs.html")

@app.route("/storage", methods = ["GET", "POST"])
@login_required
def storage():
    if request.method == "POST":
        product = request.form.get("product")
        amount = request.form.get("amount")
        price = request.form.get("price")
        type = request.form.get("type")
        date = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
        data = (product, type, amount, price, date)
        with sqlite3.connect("shop.db") as connection:
            db = connection.cursor()
            db.execute("INSERT INTO storage VALUES (?, ?, ?, ?, ?)", data)
            connection.commit()
            db.close()
        return render_template("storage.html", success = "INSERTED INTO DATABASE!") 
    else:
        info =[]
        with sqlite3.connect("shop.db") as connection:
            db0 = connection.cursor()
            for i in db0.execute("SELECT * FROM storage"):
                info.append(i)
        return render_template("storage.html", info = info)

@app.route("/login", methods = ["GET", "POST"])
def login():
    #Forget any user
    session.clear()
    if request.method == "POST":
        #Making sure user summit the require data
        if not request.form.get("name"):
            return render_template("login.html")
        elif not request.form.get("password"):
            return render_template("login.html")

        #Get user data
        info = view(request.form.get("name"))

        #Ensure name and password is correct
        text = "Invaild"
        if info == None:
            return render_template("login.html", text = text)
        if len(info) != 4 and check_password_hash(info[3], request.form.get("password")):
            return render_template("login.html", text = text)
        
        #Remember the user
        session["user_id"] = info[1]

        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/debt")
@login_required
def debt():
    return render_template("debt.html")

if __name__ ==  "__main__":
    app.run()