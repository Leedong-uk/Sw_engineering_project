from flask import Flask, session, redirect, url_for, request, render_template, flash
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'termproject2024'
cluster = MongoClient("mongodb+srv://leedonguk:1234@cluster0.xreq6mx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["term_project"]
user_collection = db["userAccount"]

@app.route('/showuserlist')
def show_user_list() :
    useraccount = list(user_collection.find({}))
    return render_template('userList.html',useraccount = useraccount)
    
