from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.ninja import Ninja
from flask_app.models.address import Address

class Dojo:
    db = 'dojos_ninjas_schema_advance'
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.address = Address.select_one(data)
        self.holds = self.select_ninjas(data)
    
    '''READ'''
    @classmethod
    def select_all(cls): #
        query = "SELECT * FROM dojos"
        results = connectToMySQL(cls.db).query_db(query)
        # 1) GET ALL ROWS FROM DB
        # [{'id': 1, 'name': 'Online', 'address_id': 1, 'created_at': datetime.datetime(2022, 3, 10, 14, 52, 17), 'updated_at': datetime.datetime(2022, 3, 10, 14, 52, 17)}, {'id': 2, 'name': 'Bellevue', 'address_id': 2, 'created_at': datetime.datetime(2022, 3, 10, 14, 52, 17), 'updated_at': datetime.datetime(2022, 3, 10, 14, 52, 17)}, {'id': 3, 'name': 'Boise', 'address_id': 3, 'created_at': datetime.datetime(2022, 3, 10, 14, 52, 17), 'updated_at': datetime.datetime(2022, 3, 10, 14, 52, 17)}, {'id': 4, 'name': 'Chicago', 'address_id': 4, 'created_at': datetime.datetime(2022, 3, 10, 14, 52, 17), 'updated_at': datetime.datetime(2022, 3, 10, 14, 52, 17)}, {'id': 5, 'name': 'Los Angeles', 'address_id': 5, 'created_at': datetime.datetime(2022, 3, 10, 14, 52, 17), 'updated_at': datetime.datetime(2022, 3, 10, 14, 52, 17)}, {'id': 6, 'name': 'Silicon Valley', 'address_id': 6, 'created_at': datetime.datetime(2022, 3, 10, 14, 52, 17), 'updated_at': datetime.datetime(2022, 3, 10, 14, 52, 17)}]
        return [cls(i) for i in results]
    

    @classmethod
    def select_one(cls, data): #
        query = "SELECT * FROM dojos WHERE dojos.id=%(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        # {'id': 1, 'name': 'Online', 'address_id': 1, 'created_at': datetime.datetime(2022, 3, 10, 14, 52, 17), 'updated_at': datetime.datetime(2022, 3, 10, 14, 52, 17)}
        # if there is ninjas in the dojo
        return cls(result[0])
    
    @classmethod
    def select_ninjas(cls, data):
        query = "SELECT * FROM ninjas WHERE dojo_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return [Ninja(i) for i in results]

    '''CREATE'''
    @classmethod
    def insert_address(cls, data):
        query = "INSERT INTO addresses(street, city, state, zip) VALUES( %(street)s , %(city)s , %(state)s , %(zip)s );"
        return connectToMySQL(cls.db).query_db(query, data)
        # returns id

    @classmethod
    def insert(cls, data):
        query="INSERT INTO dojos(name, address_id) VALUES(%(name)s, %(address_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    '''UPDATE'''
    @classmethod
    def update_address(cls, data):
        query= "UPDATE addresses SET street=%(street)s, city=%(city)s, state=%(state)s, zip=%(zip)s WHERE id = %(address_id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query="UPDATE dojos SET name=%(name)s WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    '''DELETE'''
    @classmethod
    def delete(cls,data):
        query="DELETE FROM dojos WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
        
