from http.client import EXPECTATION_FAILED
import os
from flask import Flask, Request, flash, jsonify, redirect, render_template, request, request_finished, request_started, request_tearing_down, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gohybaelwnbcfx:204db85618233783777f845b4d15e2510ff65210a62bd6898de7cc5bb30348b6@ec2-18-215-96-22.compute-1.amazonaws.com:5432/dfu3fjb6fa3fqi'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Homepage
@app.route('/')
def home():
    return render_template('home.html')

#Create an Account
class Register(db.Model):
    __tablename__ = 'register'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    con_password = db.Column(db.String(200))

    def __init__(self, username, password, con_password):
        self.username = username
        self.password = password
        self.con_password = con_password
        
@app.route('/create')
def create():
    if request.method=='POST':
        # print("Reached If")
        username=request.form['username']
        password=request.form['password']
        con_password=request.form['con_password']
        #print(username, password, con_password)
        if password != con_password:
            return render_template('create.html', message='Passwords do not match!') 
        elif username=='' or password=='' or con_password=='':
            return render_template('create.html', message='Please fill in the textboxes. Thank you.') 
        elif db.session.query(Register).filter(Register.username == username).count() == 0:
            data = Register(username, password, con_password)
            db.session.add(data)
            db.session.commit()
        elif db.session.query(Register).filter(Register.username == username).count() == 1:  
            return render_template('create.html', message="Username has been taken")
    
    return render_template('create.html')

#Sign in 
@app.route('/signin')
def signin():
    return render_template('signin.html')

