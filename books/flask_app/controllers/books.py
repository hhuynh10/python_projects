from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import book
from flask_app.models import author

@app.route('/books')
def books():
    return render_template('books.html', books = book.Book.read_books())

@app.route('/books/add', methods=['POST'])
def add_book():
    book.Book.add_book(request.form)
    return redirect('/books')

@app.route('/books/delete/<int:id>')
def delete_books(id):
    data = {'id' : id}
    book.Book.delete_book(data)
    return redirect('/books')

@app.route('/books/edit/<int:id>')
def edit_book(id):
    data = {'id' : id}
    return render_template('books_edit.html', book = book.Book.read_one_book(data))

@app.route('/books/edit', methods=['POST'])
def update_book():
    book.Book.update_book(request.form)
    return redirect('/books')

@app.route('/books/book/<int:id>')
def get_book_with_authors(id):
    data = {'id' : id}
    return render_template('book.html', book = book.Book.get__book_with_authors(data), unfavorited_authors = author.Author.unfavorited_authors(data))

@app.route('/add/favoriteAuthor', methods=['POST'])
def join_author():
    author.Author.add_favorite(request.form)
    return redirect("/")