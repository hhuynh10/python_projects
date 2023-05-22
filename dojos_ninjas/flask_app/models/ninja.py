from flask_app.config.mysqlconnection import connectToMySQL
# 1) IMPORT CONNECTION FROM CONFIG FOLDER
from flask_app.models.address import Address


class Ninja:
    db = 'dojos_ninjas_schema_advance'
    # 1) CONSTRUCT CLASS
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.dojo_id = data["dojo_id"]
        self.address = Address.select_one(data)
    
    '''READ ALL'''
    @classmethod
    def select_all(cls): #
        query = "SELECT * FROM ninjas"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(i) for i in results]
        # return a list of classes in results
        # [{'id': 13, 'name': 'xtina.codes', 'dojo_id': 1, 'dojo': 'Online', 'street': '1605 Cullen Ave', 'city': 'Chesapeake', 'state': 'VA', 'zip': 23325, 'created_at': datetime.datetime(2022, 2, 28, 22, 17, 56), 'updated_at': datetime.datetime(2022, 2, 28, 22, 17, 56)}, {'id': 14, 'name': 'Santa', 'dojo_id': 1, 'dojo': 'Online', 'street': '3945 Reindeer Way', 'city': 'North Pole', 'state': 'AL', 'zip': 99502, 'created_at': datetime.datetime(2022, 2, 28, 22, 17, 56), 'updated_at': datetime.datetime(2022, 2, 28, 22, 17, 56)}, {'id': 15, 'name': 'Stitch', 'dojo_id': 1, 'dojo': 'Online', 'street': '593 Lilo Street', 'city': 'Ocean View', 'state': 'HI', 'zip': 96737, 'created_at': datetime.datetime(2022, 2, 28, 22, 17, 56), 'updated_at': datetime.datetime(2022, 2, 28, 22, 17, 56)}, {'id': 16, 'name': 'Grace Hopper', 'dojo_id': 1, 'dojo': 'Online', 'street': '92 Programming Way', 'city': 'New York', 'state': 'NY', 'zip': 10001, 'created_at': datetime.datetime(2022, 2, 28, 22, 17, 56), 'updated_at': datetime.datetime(2022, 2, 28, 22, 17, 56)}]

    '''READ ONE'''
    @classmethod #
    def select_one(cls, data):
        query = "SELECT * FROM ninjas WHERE id=%(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        # 1) list of dictionary for row
        return cls(result[0])
        # 4) returns first dictionary converted to a class

    '''CREATE'''
    @classmethod
    def insert(cls, data):
        query="INSERT INTO ninjas(name, address_id, dojo_id) VALUES(%(name)s, %(address_id)s, %(dojo_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    '''UPDATE'''
    @classmethod
    def update(cls, data):
        query="UPDATE ninjas SET name=%(name)s, dojo_id=%(dojo_id)s WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    '''DELETE'''
    @classmethod
    def delete_address(cls,data):
        query="DELETE FROM addresses WHERE addresses.id=%(address_id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls,data):
        query="DELETE FROM ninjas WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)