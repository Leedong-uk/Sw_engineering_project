from flask import render_template, session, redirect, url_for, flash

def photo_modify(writer):
    if 'username' in session and session['username'] == writer:
        flash('작성자입니다.')
        return render_template('start_modify.html', writer=writer)
    else:
        flash('작성자가 아닙니다.')
        return redirect(url_for('homepage'))
