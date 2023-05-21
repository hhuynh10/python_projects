from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import flash

class Ride:
    db = 'ohana_rideshares'
    def __init__(self, data):
        self.id = data['id']
        self.destination = data['destination']
        self.location = data['location']
        self.date = data['date']
        self.details = data['details']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users = None

    @classmethod
    def request_ride(cls,data):
        if not cls.validate_rep_data(data):
            return False
        query = """
        INSERT INTO rides (destination, location, date, details, user_id, created_at, updated_at)
        VALUES (%(destination)s, %(location)s, %(date)s, %(details)s, %(user_id)s, NOW(), NOW())
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM rides
        LEFT JOIN users
        ON rides.user_id = users.id
        ORDER BY rides.created_at 
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        all_rides = []
        if not result:
            return result
        for this_ride in result:
            new_ride = cls(this_ride)
            data = {
                'id' : this_ride['users.id'],
                'first_name' : this_ride['first_name'],
                'last_name' : this_ride['last_name'],
                'email' : this_ride['email'],
                'password' : this_ride['password'],
                'confirm_password' : this_ride['confirm_password'],
                'created_at' : this_ride['users.created_at'],
                'updated_at' : this_ride['users.updated_at']
            }
            new_ride.users = user.User(data)
            all_rides.append(new_ride)
        return all_rides
    

    @staticmethod
    def validate_rep_data(data):
        is_valid = True
        if len(data['destination']) < 3:
            flash ('Destination must be at least 3 characters long.')
            is_valid = False
        if len(data['location']) < 3:
            flash ('Location must be at least 3 characters long.')
            is_valid = False
        if data['date'] == "":
            is_valid = False
            flash("Please enter a date")
        if len(data['details']) < 3:
            flash ('Details must be at least 10 characters long.')
            is_valid = False
        return is_valid