from flask import Flask, request, jsonify, render_template, session, redirect, url_for,flash
from pymongo import MongoClient
from datetime import datetime
import os

UPLOAD_FOLDER = 'static/user_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'termproject2024'

client = MongoClient("mongodb+srv://leedonguk:1234@cluster0.xreq6mx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["term_project"]
collection = db["Photo"]

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/posting', methods=['POST'])
def posting():
    if 'username' not in session:
        flash("로그인 후 이용하세요.")
        return redirect(url_for('homepage'))

    else :
        username = session['username']
        title_receive = request.form['image_title']
        keyword_receive = request.form['image_keyword']
        description_receive = request.form['image_description']
        file = request.files['image_file']
        today = datetime.now()
        mytime = today.strftime('%Y%m%d%H%M%S')
        filename = f'{mytime}-{file.filename}'
        save_to = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not (title_receive and keyword_receive and filename and username and description_receive):
            flash("모든 정보를 다 입력하세요.")
            return redirect(url_for('upload'))

        file.save(save_to)
    
        doc = {
            'title': title_receive,
            'keyword': keyword_receive,
            'file': filename,
            'username': username,
            'description':description_receive
            }
        collection.insert_one(doc)
        print("Redirecting to homepage")
        flash("업로드완료")
        return redirect(url_for('homepage'))


