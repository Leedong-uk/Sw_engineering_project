from flask import Flask, session, redirect, url_for
from Login import login as login_function, logout as logout_function
from Register import register as register_function

app = Flask(__name__)
app.config['SECRET_KEY'] = 'termproject2024'

@app.route('/hompage')
def homepage():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/', methods=['GET', 'POST'])
def login():
    return login_function()

@app.route('/logout')
def logout():
    return logout_function()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_function()

if __name__ == '__main__':
    app.run(debug=True)
