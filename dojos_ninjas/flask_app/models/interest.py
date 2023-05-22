from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.ninja import Ninja

class Interest:
    db = 'dojos_ninjas_schema_advance'
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.holds = []
    
    '''READ ALL'''
    @classmethod
    def select_all(cls):
        query = "SELECT * FROM interests"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(i) for i in results]
    
    '''READ ONE'''
    @classmethod
    def select_one(cls, data):
        query = "SELECT * FROM ninjas_interests LEFT JOIN interests ON interests.id = ninjas_interests.interest_id LEFT JOIN ninjas ON ninjas.id = ninjas_interests.ninja_id WHERE interest_id = %(interest_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        # 1) many to many join
        if results: 
        # if [{'id': 18, 'ninja_id': 3, 'interest_id': 5, 'created_at': datetime.datetime(2022, 3, 15, 8, 31, 15), 'updated_at': datetime.datetime(2022, 3, 15, 8, 31, 15), 'interests.id': 5, 'name': 'test', 'description': 'ing', 'interests.created_at': datetime.datetime(2022, 3, 15, 8, 28, 42), 'interests.updated_at': datetime.datetime(2022, 3, 15, 8, 28, 42), 'ninjas.id': 3, 'ninjas.name': 'Stitch', 'ninjas.created_at': datetime.datetime(2022, 3, 10, 14, 46, 37), 'ninjas.updated_at': datetime.datetime(2022, 3, 10, 14, 56, 15), 'address_id': 9, 'dojo_id': 5}]
        # 2) if there are ninjas
            interest = {
            # 2a) setup interest CLASS DATA DICT with results
                    "id": results[0]["interest_id"],
                    "name": results[0]["name"],
                    "description": results[0]["description"]
                }
            x = cls( interest )
            # 2b) INITIATE interest CLASS
            for i in results:
            # 2c) go through EACH RESULT
                e = {"id" : i["ninjas.id"]}
                # create DICT to pass using ninja ID from RESULTS
                x.holds.append( Ninja.select_one(e) )
                # 2d) initiate NINJA OBJECT using the select_one function with id
                # 2d) APPEND ninja object to interest.holds
            return x
            # 3) return interests holds ninjas
        else:
        # elif ()
        # 2) if there are no users
            query = "SELECT * FROM interests WHERE id=%(interest_id)s"
            result = connectToMySQL(cls.db).query_db(query, data)
            return cls(result[0])
            # {'id': 7, 'name': 'nothing', 'description': 'none', 'created_at': datetime.datetime(2022, 3, 15, 11, 1, 38), 'updated_at': datetime.datetime(2022, 3, 15, 11, 1, 38)}
            # 3) return intererst 

    '''GET INTERESTS FOR NINJA'''
    @classmethod
    def get_interests(cls, data):
        query = "SELECT * FROM ninjas_interests LEFT JOIN interests ON interests.id = ninjas_interests.interest_id WHERE ninja_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return [cls(i) for i in results]

    '''CREATE'''
    @classmethod
    def insert(cls, data):
        query="INSERT INTO interests(name, description) VALUES(%(name)s, %(description)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def insert_ninjas_interests(cls, data):
        query="INSERT INTO ninjas_interests(ninja_id, interest_id) VALUES(%(ninja_id)s, %(interest_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    '''UPDATE'''
    @classmethod
    def update(cls, data):
        query="UPDATE interests SET name=%(name)s, description=%(description)s WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    '''DELETE'''
    @classmethod
    def delete_interest_ninja(cls, data):
        query="DELETE FROM ninjas_interests WHERE ninja_id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query="DELETE FROM interests WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query,data)