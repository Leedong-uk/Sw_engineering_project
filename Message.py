# Message.py

from flask import session, redirect, url_for, render_template, request, jsonify, flash
from datetime import datetime
from bson import ObjectId

def message(messages_collection, users_collection):
    if 'username' in session:
        current_user = session['username']
        senders_to_me = messages_collection.distinct('sender', {'receiver': current_user})
        senders_from_me = messages_collection.distinct('receiver', {'sender': current_user})
        senders_to_me = [sender for sender in senders_to_me if sender != current_user]
        senders_from_me = [sender for sender in senders_from_me if sender != current_user]
        all_senders = list(set(senders_to_me + senders_from_me))
        users = users_collection.find({'username': {'$in': all_senders}}, {"username": 1, "_id": 0})
        return render_template('message.html', users=users)
    return redirect(url_for('login'))

def chat(messages_collection, users_collection, username):
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

def notifications(messages_collection):
    if 'username' in session:
        current_user = session['username']
        new_messages_count = messages_collection.count_documents({'receiver': current_user, 'read': False})
        return jsonify({'new_messages': new_messages_count})
    return redirect(url_for('login'))

def delete_message(messages_collection, message_id):
    if 'username' in session:
        current_user = session['username']

        message = messages_collection.find_one({'_id': ObjectId(message_id), 'sender': current_user})

        if message:
            messages_collection.delete_one({'_id': ObjectId(message_id)})
            flash('메시지가 삭제되었습니다.')
        else:
            flash('메시지를 삭제할 수 없습니다.')

        return redirect(url_for('chat', username=message['receiver'] if message else ''))
    return redirect(url_for('login'))
