from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app

class Comment:
    db = 'dojo_wall'
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
    
    @classmethod
    def post_comment(cls,data):
        query = """
        INSERT INTO comments (comment, created_at, updated_at, user_id, post_id)
        VALUES (%(comment)s, NOW(), NOW(), %(user_id)s, %(post_id)s)
        ;"""
        comment_id = connectToMySQL(cls.db).query_db(query, data)
        return comment_id