from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import author
from flask_app.models import book

@app.route('/')
def index():
    return redirect('/authors')

@app.route('/authors')
def authors_page():
    return render_template('authors.html', authors = author.Author.read_authors())

@app.route('/authors/add', methods=['POST'])
def add_author():
    author.Author.add_author(request.form)
    return redirect('/')

@app.route('/authors/delete/<int:id>')
def delete_author(id):
    data = {'id' : id}
    author.Author.delete_author(data)
    return redirect('/')

@app.route('/authors/edit/<int:id>')
def edit_author(id):
    data = {'id' : id}
    return render_template('authors_edit.html', author = author.Author.read_one_author(data))

@app.route('/authors/edit', methods=['POST'])
def update():
    author.Author.update_author(request.form)
    return redirect('/')

@app.route('/authors/author/<int:id>')
def get_author_with_books(id):
    data = {'id' : id}
    return render_template('author.html', author = author.Author.get_author_with_books(data), unfavorited_books = book.Book.unfavorited_books(data))

@app.route('/add/favorite', methods=['POST'])
def join_book():
    author.Author.add_favorite(request.form)
    return redirect("/")

