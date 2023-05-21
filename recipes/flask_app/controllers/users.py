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
        return redirect ('/recipes')
    return redirect ('/')

@app.route('/users/login', methods = ['POST'])
def login():
    if user.User.login(request.form):
        return redirect('/recipes')
    return redirect('/')

@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/view/<int:id>')
def view_user(id):
    if 'user_id' not in session:
        return redirect ('/users/logout')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('view_user.html', user = user.User.get_user_by_id(id), this_user = this_user)

@app.route('/users/delete/<int:id>')
def delete_user(id):
    user.User.delete_user(id)
    return redirect ('/')