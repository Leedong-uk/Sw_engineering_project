from flask import Flask, session, redirect, url_for, render_template, flash, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

from Login import login as login_function, logout as logout_function
from Upload import upload as upload_function, posting as posting_function
from Homepage import homepage as homepage_function, search as search_function
from Register import register as register_function
from Photo_detail import photo_detail as photo_detail_function
from Photo_modify import photo_modify as photo_modify_function, revise as revise_function
from UserList import show_user_list as show_user_list_function
from Message import message as message_function, chat as chat_function, notifications as notifications_function, delete_message as delete_message_function

app = Flask(__name__)
app.secret_key = 'termproject2024'
cluster = MongoClient("mongodb+srv://leedonguk:1234@cluster0.xreq6mx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["term_project"]
users_collection = db["userAccount"]
messages_collection = db["message"]

@app.route('/')
def homepage():
    return homepage_function()

@app.route('/upload')
def upload():
    return upload_function()

@app.route('/posting', methods=['POST'])
def posting():
    return posting_function()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_function()

@app.route('/logout')
def logout():
    return logout_function()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_function()

@app.route('/photodetail/<photo_id>')
def photodetail(photo_id):
    return photo_detail_function(photo_id)

@app.route('/photomodify/<photo_id>') 
def photomodify(photo_id):
    return photo_modify_function(photo_id)

@app.route('/revise/<photo_id>', methods=['POST'])
def revise(photo_id):
    return revise_function(photo_id)

@app.route('/showuserlist')
def show():
    return show_user_list_function()

@app.route('/search/<keyword>')
def search(keyword):
    return search_function(keyword)

@app.route('/message/')
def message():
    return message_function(messages_collection, users_collection)

@app.route('/message/<username>', methods=['GET', 'POST'])
def chat(username):
    return chat_function(messages_collection, users_collection, username)

@app.route('/notifications')
def notifications():
    return notifications_function(messages_collection)

@app.route('/deletemessage/<message_id>', methods=['POST'])
def delete_message(message_id):
    return delete_message_function(messages_collection, message_id)

if __name__ == '__main__':
    app.run(debug=True)
