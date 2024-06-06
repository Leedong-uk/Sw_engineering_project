from flask import Flask, session, render_template, request
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'termproject2024'

cluster = MongoClient("mongodb+srv://leedonguk:1234@cluster0.xreq6mx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["term_project"]
photo_collection = db["Photo"]

@app.route('/')
def homepage():
    if 'username' not in session:
        photos = list(photo_collection.find({}))
        return render_template('not_login_homepage.html', photos=photos)
    else:
        photos = list(photo_collection.find({}))
        return render_template('login_homepage.html', photos=photos)

@app.route('/search/<keyword>')
def search(keyword):
    if keyword:
        photos = list(photo_collection.find({"keyword": keyword}))
    else:
        photos = list(photo_collection.find({}))
    return render_template('login_homepage.html', photos=photos)


