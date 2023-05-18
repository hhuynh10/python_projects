from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

class User:
    db = 'dojo_wall'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.confirm_password = data['confirm_password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []
    
# CREATE SQL
    @classmethod
    def create_user(cls,data):
        if not cls.validate_reg_data(data):
            return False
        parsed_data = cls.parse_reg_data(data)
        query = """
        INSERT INTO users (first_name, last_name, email, password, confirm_password, created_at, updated_at)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(confirm_password)s, NOW(), NOW())
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query, parsed_data)
        session['user_id'] = user_id
        return user_id
    
# READ SQL
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email}
        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        if result:
            result = cls(result[0])
        return result
    
    @classmethod
    def get_user_by_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT * FROM users
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result

# UPDATE SQL
    # @classmethod
    # def update_user(cls, id):
    #     query = """
    #     UPDATE users
    #     SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, confirm_password = %(confirm_password)s, created_at = NOW(), updated_at = NOW()
    #     WHERE id = %(id)s
    #     ;"""
    #     return connectToMySQL(cls.db).query_db(query, id)

# DELETE SQL
    @classmethod
    def delete_user(cls, id):
        data = {'id' : id}
        query = """
        DELETE FROM users
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

# Validate SQL
    @staticmethod
    def validate_reg_data(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash ('Your first name must be at least 2 characters long.', 'register')
            is_valid = False
        if len(data['last_name']) < 2:
            flash ('Your last name must be at least 2 characters long.','register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash ('Email is not valid.', 'register')
            is_valid = False
        if User.get_user_by_email(data['email'].lower()):
            flash ('Email is already in use.', 'register')
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash ('Your password must be minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character.', 'register')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash ('Your passwords do not match.', 'register')
            is_valid = False
        return is_valid
    
    @staticmethod
    def parse_reg_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['email'] = data['email'].lower()
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        parsed_data['confirm_password'] = data['confirm_password']
        return parsed_data

    @staticmethod
    def login(data):
        this_user = User.get_user_by_email(data['email'].lower())
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                return True
        flash ('Your login info is incorrect.', 'login')
        return False