import pymongo
from pymongo import MongoClient
from flask import render_template, redirect, url_for, flash
from Form import RegistrationForm

def register():
    cluster  = MongoClient("mongodb+srv://leedonguk:1234@cluster0.xreq6mx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = cluster["term_project"]
    collection = db["userAccount"]
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        if collection.find_one({"email": email}):
            flash('이미 존재하는 이메일입니다')
        else:
            user_account = {
                "username" : username,
                "email": email,
                "password": password
            }
            result = collection.insert_one(user_account)
            if result.acknowledged:
                flash("회원가입이 완료되었습니다")
                return redirect(url_for('login'))
            else:
                flash("회원가입에 실패하였습니다")
    
    return render_template('register.html', form=form)
