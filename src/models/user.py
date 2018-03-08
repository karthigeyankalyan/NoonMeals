import uuid

from flask import session

from src.common.database import Database

class User(object):
    def __init__(self, email, password, username, _id=None):
        self.email = email
        self.password = password
        self.username = username
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one('users', {'email': email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_username(cls, username):
        data = Database.find_one('users', {'username': username})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one('users', {'_id': _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def valid_login(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password, username):
        user = cls.get_by_email(email)
        if user is None:
            new_user = User(email, password, username)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def json(self):
        return{
            'email': self.email,
            '_id': self._id,
            'password': self.password,
            'username': self.username
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())