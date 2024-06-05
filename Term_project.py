from datetime import datetime
from flask import Flask, session, redirect, url_for, render_template, request, jsonify
from pymongo import MongoClient
from Login import login as login_function, logout as logout_function
from Upload import upload as upload_function, posting as posting_function
from Homepage import homepage as homepage_function
from Register import register as register_function

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

@app.route('/message/')
def message():
    if 'username' in session:
        users = users_collection.find({}, {"username": 1, "_id": 0})
        return render_template('message.html', users=users)
    return redirect(url_for('login'))

@app.route('/message/<username>', methods=['GET', 'POST'])
def chat(username):
    if 'username' in session:
        current_user = session['username']
        if request.method == 'POST':
            message = request.form.get('message')
            if message:
                timestamp = datetime.datetime.now()
                messages_collection.insert_one({
                    'sender': current_user,
                    'receiver': username,
                    'message': message,
                    'timestamp': timestamp,
                    'read': False
                })


        messages_collection.update_many(
            {'receiver': session['username'], 'sender': username, 'read': False},
            {'$set': {'read': True}}
        )


        messages = list(messages_collection.find({
            '$or': [
                {'sender': current_user, 'receiver': username},
                {'sender': username, 'receiver': current_user}
            ]
        }).sort('timestamp'))

        return render_template('chat.html', messages=messages, username=username)
    return redirect(url_for('login'))

@app.route('/notifications')
def notifications():
    if 'username' in session:
        current_user = session['username']
        new_messages_count = messages_collection.count_documents({'receiver': current_user, 'read': False})
        return jsonify({'new_messages': new_messages_count})
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
