from flask import Flask, session, redirect, url_for, request, render_template, flash
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'termproject2024'
cluster = MongoClient("mongodb+srv://leedonguk:1234@cluster0.xreq6mx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["term_project"]
collection = db["userAccount"]

def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user = collection.find_one({"email": email, "password": password})
            if user:
                session['username'] = user['username']
                return redirect(url_for('homepage'))
            else:
                flash('로그인 실패')
        else:
            flash('모든 필드를 입력해주세요.')
    return render_template('login.html')

def logout():
    session.pop('username', None)
    return redirect(url_for('homepage'))
