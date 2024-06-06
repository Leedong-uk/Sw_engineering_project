from flask import Flask, session, redirect, url_for, render_template, flash
from Login import login as login_function, logout as logout_function
from Upload import upload as upload_function, posting as posting_function
from Homepage import homepage as homepage_function, search as search_function
from Register import register as register_function
from Photo_detail import photo_detail as photo_detail_function
from Photo_modify import photo_modify as photo_modify_function, revise as revise_function
from UserList import show_user_list as show_user_list_function

app = Flask(__name__)
app.secret_key = 'termproject2024'

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

if __name__ == '__main__':
    app.run(debug=True)
