from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    db = 'books_project'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []

    @classmethod
    def add_author(cls, data):
        query = """
        INSERT INTO authors (name, created_at, updated_at)
        VALUES (%(name)s, NOW(), NOW())
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def read_authors(cls):
        query= """
        SELECT *
        FROM authors
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        authors = []
        for author in result:
            authors.append(cls(author))
        return authors
    
    @classmethod
    def read_one_author(cls, data):
        query = """
        SELECT * FROM authors
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_author_with_books(cls,data):
        query = """
        SELECT * FROM authors 
        LEFT JOIN favorites ON authors.id = favorites.author_id 
        LEFT JOIN books ON books.id = favorites.book_id 
        WHERE authors.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)

        # Creates instance of author object from row one
        author = cls(results[0])
        # append all book objects to the instances favorites list.
        for row in results:
            # if there are no favorites
            if row['books.id'] == None:
                break
            # common column names come back with specific tables attached
            data = {
                "id": row['books.id'],
                "title": row['title'],
                "num_of_pages": row['num_of_pages'],
                "created_at": row['books.created_at'],
                "updated_at": row['books.updated_at']
            }
            author.books.append(book.Book(data))
        return author
    
    @classmethod
    def unfavorited_authors(cls,data):
        query = """
        SELECT * FROM authors 
        WHERE authors.id 
        NOT IN ( SELECT author_id FROM favorites WHERE book_id = %(id)s );
        """
        authors = []
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            authors.append(cls(row))
        return authors
    
    @classmethod
    def add_favorite(cls,data):
        query = """
        INSERT INTO favorites (author_id, book_id) 
        VALUES (%(author_id)s,%(book_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_author(cls, data):
        query = """
        DELETE FROM authors
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def update_author(cls, data):
        query = """
        UPDATE authors
        SET name = %(name)s
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)