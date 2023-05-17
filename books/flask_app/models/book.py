from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    db = 'books_project'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []

    @classmethod
    def add_book(cls, data):
        query = """
        INSERT INTO books (title, num_of_pages, created_at, updated_at)
        VALUES (%(title)s, %(num_of_pages)s, NOW(), NOW())
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def read_books(cls):
        query= """
        SELECT *
        FROM books
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        books = []
        for book in result:
            books.append(cls(book))
        return books
    
    @classmethod
    def read_one_book(cls, data):
        query = """
        SELECT * FROM books
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def delete_book(cls, data):
        query = """
        DELETE FROM books
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def update_book(cls, data):
        query = """
        UPDATE books
        SET title = %(title)s, num_of_pages = %(num_of_pages)s
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def unfavorited_books(cls,data):
        query = """
        SELECT * FROM books 
        WHERE books.id 
        NOT IN ( SELECT book_id FROM favorites WHERE author_id = %(id)s );
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        books = []
        for row in results:
            books.append(cls(row))
        print(books)
        return books
    
    @classmethod
    def get__book_with_authors(cls,data):
        query = """
        SELECT * FROM books 
        LEFT JOIN favorites ON books.id = favorites.book_id 
        LEFT JOIN authors ON authors.id = favorites.author_id 
        WHERE books.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        book = cls(results[0])
        for row in results:
            if row['authors.id'] == None:
                break
            data = {
                "id": row['authors.id'],
                "name": row['name'],
                "created_at": row['authors.created_at'],
                "updated_at": row['authors.updated_at']
            }
            book.authors.append(author.Author(data))
        return book