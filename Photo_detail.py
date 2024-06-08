from flask import render_template
from bson.objectid import ObjectId
import pymongo

cluster = pymongo.MongoClient("mongodb+srv://leedonguk:1234@cluster0.xreq6mx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["term_project"]
photo_collection = db["Photo"]

def photo_detail(photo_id):
    photo = photo_collection.find_one({"_id": ObjectId(photo_id)})
    if photo:
        uploader = photo.get('username')
        return render_template('photo_detail.html', photo=photo, uploader=uploader)
    else:
        return "Photo not found", 404
