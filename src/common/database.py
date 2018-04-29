import os

import pymongo

class Database(object):
    URI = os.environ['MONGODB_URI']
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['heroku_sc2xc25q']

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
    def update_employee(collection, query, emp_name, district, block, panchayat, designation, center_name, dob, doj, dor):
        return Database.DATABASE[collection].update_one(query, {'$set':{'Employee Name':emp_name,
                                                                        'District':district,
                                                                        'Block': block,
                                                                        'Name Of Village Panchayat': panchayat,
                                                                        'Designation': designation,
                                                                        'Name of the Center': center_name,
                                                                        'Date Of Birth': dob,
                                                                        'Date Of Joining': doj,
                                                                        'Date Of Retirement': dor}}, True)
