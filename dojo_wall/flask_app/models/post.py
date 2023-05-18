from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import flash, session

class Post:
    db = 'dojo_wall'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.users = None
    
    # CREATE SQL
    @classmethod
    def create_post(cls,data):
        if not cls.validate_rep_data(data):
            return False
        query = """
        INSERT INTO posts (content, created_at, updated_at, user_id)
        VALUES (%(content)s, NOW(), NOW(), %(user_id)s)
        ;"""
        post_id = connectToMySQL(cls.db).query_db(query, data)
        return post_id
    
    # READ SQL
    @classmethod
    def view_all_posts(cls):
        query = """
        SELECT * 
        FROM posts
        LEFT JOIN users
        ON users.id = posts.user_id
        ORDER BY posts.created_at DESC
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        all_posts = []
        if not result:
            return result
        for this_post in result:
            new_post = cls(this_post)
            this_rep = {
                'id' : this_post['users.id'],
                'first_name' : this_post['first_name'],
                'last_name' : this_post['last_name'],
                'email' : this_post['email'],
                'password' : this_post['password'],
                'confirm_password' : this_post['confirm_password'],
                'created_at' : this_post['users.created_at'],
                'updated_at' : this_post['users.updated_at']
            }
            new_post.users = user.User(this_rep)
            all_posts.append(new_post)
        return all_posts
    
    @classmethod
    def view_one_post(cls, id):
        data = {'id' : id}
        query = """
        SELECT *
        FROM posts
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result
    
    # DELETE SQL
    @classmethod
    def delete_post(cls, id):
        data = {'id' : id}
        query = """
        DELETE FROM posts
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    # UPDATE SQL
    @classmethod
    def update_post(cls, id):
        query = """
        UPDATE posts
        SET content = %(content)s, created_at = NOW(), updated_at = NOW()
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, id)
    
    # VALIDATE SQL
    @staticmethod
    def validate_rep_data(data):
        is_valid = True
        if len(data['content']) < 1:
            flash ('Content must not be blank.')
            is_valid = False
        return is_valid