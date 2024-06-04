from flask import session, render_template

def homepage():
    if 'username' not in session:
        print("No username in session")  # 디버깅 메시지
        return render_template('not_login_homepage.html')
    else:
        print("Username in session:", session['username'])  # 디버깅 메시지
        return render_template('login_homepage.html')
