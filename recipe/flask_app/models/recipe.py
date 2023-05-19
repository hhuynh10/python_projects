from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import flash

class Recipe:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under30 = data['under30']
        self.user_id = data['user_id']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        self.users = None
    
    @classmethod
    def create_recipe(cls,data):
        if not cls.validate_rep_data(data):
            return False
        query = """
        INSERT INTO recipes (name, description, instructions, date, under30, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under30)s, %(user_id)s)
        ;"""
        recipe_id = connectToMySQL(cls.db).query_db(query, data)
        return recipe_id
    
    @classmethod
    def view_all_recipes(cls):
        query = """
        SELECT * FROM recipes
        LEFT JOIN users
        ON recipes.user_id = users.id
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        if not result:
            return result
        for this_recipe in result:
            new_recipe = cls(this_recipe)
            this_rep = {
                'id' : this_recipe['users.id'],
                'first_name' : this_recipe['first_name'],
                'last_name' : this_recipe['last_name'],
                'email' : this_recipe['email'],
                'password' : this_recipe['password'],
                'confirm_password' : this_recipe['confirm_password'],
                'created_at' : this_recipe['users.created_at'],
                'updated_at' : this_recipe['users.updated_at']
            }
            new_recipe.users = user.User(this_rep)
            all_recipes.append(new_recipe)
        return all_recipes
    

    @staticmethod
    def validate_rep_data(data):
        is_valid = True
        if len(data['name']) < 3:
            flash ('Name must be at least 3 characters long.')
            is_valid = False
        if len(data['description']) < 3:
            flash ('Description must be at least 3 characters long.')
            is_valid = False
        if len(data['instructions']) < 3:
            flash ('Instructions must be at least 3 characters long.')
            is_valid = False
        if data['date'] == "":
            is_valid = False
            flash("Please enter a date")
        return is_valid