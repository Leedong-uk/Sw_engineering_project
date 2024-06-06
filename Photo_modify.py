from flask import render_template, session, redirect, url_for, flash, request
from bson.objectid import ObjectId
import pymongo
import os
from datetime import datetime

# MongoDB 연결 설정
cluster = pymongo.MongoClient("mongodb+srv://leedonguk:1234@cluster0.xreq6mx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["term_project"]
photo_collection = db["Photo"]

def photo_modify(photo_id):
    photo = photo_collection.find_one({"_id": ObjectId(photo_id)})
    writer = photo['username']
    
    if 'username' in session and session['username'] == writer:
        flash('사진정보를 수정합니다')
        return render_template('start_modify.html', photo=photo)
    else:
        flash('작성자가 아닙니다.')
        return redirect(url_for('homepage'))

def revise(photo_id):
    photo = photo_collection.find_one({"_id": ObjectId(photo_id)})

    if not photo:
        flash("해당 사진을 찾을 수 없습니다.")
        return redirect(url_for('homepage'))

    username = session.get('username')
    title_receive = request.form.get('image_title')
    keyword_receive = request.form.get('image_keyword')
    description_receive = request.form.get('image_description')
    file = request.files.get('image_file')  # 파일이 없을 경우 None 반환

    if not (title_receive and keyword_receive and description_receive):
        flash("모든 정보를 다 입력하세요.")
        return redirect(url_for('photomodify', photo_id=photo_id))

    update_fields = {
        'title': title_receive,
        'keyword': keyword_receive,
        'description': description_receive
    }

    if file and file.filename != '':
        today = datetime.now()
        mytime = today.strftime('%Y%m%d%H%M%S')
        filename = f'{mytime}-{file.filename}'
        save_to = os.path.join('static/user_images', filename)
        file.save(save_to)
        update_fields['file'] = filename
    else:
        update_fields['file'] = photo['file']  # 기존 파일 유지

    photo_collection.update_one(
        {"_id": ObjectId(photo_id)},
        {"$set": update_fields}
    )
    
    flash("수정이 완료되었습니다.")
    return redirect(url_for('homepage'))
