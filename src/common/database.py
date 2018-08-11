import os

import pymongo
from bson import ObjectId
from bson.errors import InvalidId


class Database(object):
    URI = os.environ['MONGODB_URI']
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['heroku_sc2xc25q']

    # URI = "mongodb://127.0.0.1:27017"
    # DATABASE = None
    #
    # @staticmethod
    # def initialize():
    #     client = pymongo.MongoClient(Database.URI)
    #     Database.DATABASE = client['NMP']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def is_valid(oid):
        try:
            ObjectId(oid)
            return True
        except (InvalidId, TypeError):
            return False

    @staticmethod
    def update_employee(collection, query, emp_name, district, block, panchayat, designation, center_name, dob, doj,
                        dor, joining_date_current_post, nhis_id, gender):
        return Database.DATABASE[collection].update_one(query, {'$set': {'Employee Name': emp_name,
                                                                         'District': district,
                                                                         'Block': block,
                                                                         'Name of Village Panchayat': panchayat,
                                                                         'Designation': designation,
                                                                         'Name of the Center': center_name,
                                                                         'Date of Birth': dob,
                                                                         'joining_date_current_post':
                                                                             joining_date_current_post,
                                                                         'nhis_id': nhis_id,
                                                                         'gender': gender,
                                                                         'Date of Joining': doj,
                                                                         'Date of Retirement': dor}}, True)
    @staticmethod
    def delete_from_mongo(collection, query):
        print(query)
        Database.DATABASE[collection].remove(query)
