from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user

@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def users():
    return render_template('index.html')

@app.route('/users/register', methods = ['POST'])
def register():
    if user.User.create_user(request.form):
        return redirect ('/rides/dashboard')
    return redirect ('/')

@app.route('/users/login', methods = ['POST'])
def login():
    if user.User.login(request.form):
        return redirect('/rides/dashboard')
    return redirect('/')

@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')