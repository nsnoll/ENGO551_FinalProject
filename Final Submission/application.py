from asyncio.windows_events import NULL
from audioop import avg
import os
from cachelib import NullCache
import requests

from flask import Flask, jsonify, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine, null
from sqlalchemy.orm import scoped_session, sessionmaker



app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#change styling
#fix register, logout, log in
@app.route("/", methods=["POST","GET"])
def index():
    if request.method=="GET":
        if session.get("username") is None:
            #change this to not have navbar
            return render_template("index.html")
        else:
            message="You are already logged in."
            return render_template("message.html", message=message)
    else:
        message="You have successfully logged out."
        session["username"]=None
        session["password"]=None
        return render_template("message.html", message=message)

@app.route("/register", methods=["POST"])
def register():
        session["username"] = request.form.get("username")
        session["password"] = request.form.get("password")
        
        #check if register or login
        
        # check if username exists
        dbusername=db.execute("SELECT * FROM users WHERE username= :user",
            {"user": session["username"]}).fetchone()

        if dbusername is None:
            #if username doesnt exist
            #else:
            #register
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                        {"username":session["username"], "password": session["password"]})
            db.commit()
            message="You've successfuly registered an account. Please log in."
            session["username"]=None
            session["password"]=None
            return render_template("login.html",message=message)

            #if username exists
        else:
            message= "This username already exists."
            session["username"]=None
            session["password"]=None
            return render_template("message.html", message=message)

@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method=="GET":
        if session["username"] is None:
            message="Please log in first."
            return render_template("message.html",message=message)
        else:
            message= "Welcome, "
            return render_template("search.html", username=session["username"], message=message)

    
    else:
        
        session["username"] = request.form.get("username")
        session["password"] = request.form.get("password")
        
        #check if register or login
        
        # check if username exists
        dbusername=db.execute("SELECT * FROM users WHERE username= :user",
            {"user": session["username"]}).fetchone()

        if dbusername is None:
                #if username doesnt exist

            message= "This username does not exist.";
            session["username"]=None
            session["password"]=None
            return render_template("message.html", message=message)

            #if username exists
        else:
        #login
        #check if the password matches
            if dbusername[1]==session["password"]:
                #if it matches then 
                message= "Welcome, "
                return render_template("search.html", username=session["username"], message=message)
            else:    
            #if it doesnt match
            #error
                message= "It seems like you have forgot your password."
                session["username"]=None
                session["password"]=None
                return render_template("message.html", message=message)

@app.route("/locate", methods=["POST"])
def locate():
    return render_template("locate.html")

@app.route("/results", methods=["POST"])
def results():
        if int(results.rowcount) == 0:
            message="No results available."
            return render_template("message.html", message=message)
        else:
            return render_template("results.html", results=results)
