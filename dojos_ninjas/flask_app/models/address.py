from flask_app.config.mysqlconnection import connectToMySQL

class Address:
    db = 'dojos_ninjas_schema_advance'
    def __init__(self, data):
        self.id = data["id"]
        self.street = data["street"]
        self.city = data["city"]
        self.state = data["state"]
        self.zip = data["zip"]
    
    '''READ'''
    @classmethod
    def select_one(cls,data):
        query="SELECT * FROM addresses WHERE id=%(address_id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    '''CREATE'''
    @classmethod
    def insert(cls, data):
        query="INSERT INTO addresses(street, city, state, zip) VALUES(%(street)s, %(city)s, %(state)s, %(zip)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    '''UPDATE'''
    @classmethod
    def update(cls, data):
        query="UPDATE addresses SET street=%(street)s, city=%(city)s, state=%(state)s, zip=%(zip)s WHERE address id=%(address_id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    '''DELETE'''
    @classmethod
    def delete(cls, data):
        query="DELETE FROM addresses WHERE id=%(address_id)s"
        return connectToMySQL(cls.db).query_db(query, data)