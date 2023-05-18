from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect ('/users/logout')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('dashboard.html', this_user = this_user, posts = post.Post.view_all_posts())

@app.route('/posts/create', methods = ['POST'])
def create_report():
    if post.Post.create_post(request.form):
        return redirect ('/dashboard')
    return redirect ('/dashboard')

@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post.Post.delete_post(id)
    return redirect ('/dashboard')

@app.route('/posts/edit/<int:id>')
def edit_post(id):
    if 'user_id' not in session:
        return redirect ('/users/logout')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template("edit_post.html", this_user = this_user, post = post.Post.view_one_post(id))

@app.route('/posts/edit/post', methods = ['POST'])
def edit():
    id = request.form['id']
    if not post.Post.validate_rep_data(request.form):
        return redirect (f"/posts/edit/{id}")
    post.Post.update_post(request.form)
    return redirect ('/dashboard')