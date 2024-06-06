from flask import session, render_template
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://leedonguk:1234@cluster0.xreq6mx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["term_project"]
photo_collection = db["Photo"]

def homepage():
    if 'username' not in session:
        print("No username in session")
        photos = list(photo_collection.find({}))
        return render_template('not_login_homepage.html',photos = photos)
    else:
        print("Username in session:", session['username'])
        photos = list(photo_collection.find({}))
        return render_template('login_homepage.html', photos=photos)
