from datetime import datetime

from bson import ObjectId
from flask import Flask, session, redirect, url_for, render_template, flash, request, jsonify
from pymongo import MongoClient

from Login import login as login_function, logout as logout_function
from Upload import upload as upload_function, posting as posting_function
from Homepage import homepage as homepage_function, search as search_function
from Register import register as register_function
from Photo_detail import photo_detail as photo_detail_function
from Photo_modify import photo_modify as photo_modify_function, revise as revise_function
from UserList import show_user_list as show_user_list_function

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
    if 'username' in session:
        current_user = session['username']
        # 나에게 메시지를 보낸 적이 있는 사용자와 내가 보낸 메시지를 모두 포함하는 사용자 목록 추출
        senders_to_me = messages_collection.distinct('sender', {'receiver': current_user})
        senders_from_me = messages_collection.distinct('receiver', {'sender': current_user})
        # 나 자신은 제외
        senders_to_me = [sender for sender in senders_to_me if sender != current_user]
        senders_from_me = [sender for sender in senders_from_me if sender != current_user]
        # 중복을 제거한 후 모든 보낸 메시지와 받은 메시지의 사용자 목록 결합
        all_senders = list(set(senders_to_me + senders_from_me))
        # 해당 사용자 목록으로 유저 조회
        users = users_collection.find({'username': {'$in': all_senders}}, {"username": 1, "_id": 0})
        return render_template('message.html', users=users)
    return redirect(url_for('login'))

@app.route('/message/<username>', methods=['GET', 'POST'])
def chat(username):
    if 'username' in session:
        current_user = session['username']
        if request.method == 'POST':
            message = request.form.get('message')
            if message:
                timestamp = datetime.now()
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


@app.route('/deletemessage/<message_id>', methods=['POST'])
def delete_message(message_id):
    if 'username' in session:
        current_user = session['username']

        # 메시지 ID로 해당 메시지를 찾고, 보낸 사람이 현재 사용자와 일치하는지 확인
        message = messages_collection.find_one({'_id': ObjectId(message_id), 'sender': current_user})

        if message:
            messages_collection.delete_one({'_id': ObjectId(message_id)})
            flash('메시지가 삭제되었습니다.')
        else:
            flash('메시지를 삭제할 수 없습니다.')

        return redirect(url_for('chat', username=message['receiver'] if message else ''))
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
