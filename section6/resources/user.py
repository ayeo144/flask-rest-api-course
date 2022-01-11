import sqlite3

from flask_restful import Resource, reqparse


class User:

    # using _id isntead of id, as id is a python keyword
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT * FROM users WHERE username=?"""
        result = cursor.execute(query, (username, )) # parameters always have to be in form of a tuple
        row = result.fetchone() # gets the first row from the result set

        if row is not None:
            user = cls(*row)
        else:
            user = None

        connection.close()

        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT * FROM users WHERE id=?"""
        result = cursor.execute(query, (_id, )) # parameters always have to be in form of a tuple
        row = result.fetchone() # gets the first row from the result set

        if row is not None:
            user = cls(*row)
        else:
            user = None

        connection.close()

        return user


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):

        data = UserRegister.parser.parse_args()

        user = User.find_by_username(data['username'])
        if user is not None:
            return {'message': 'Username already exists!'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """INSERT INTO users VALUES (NULL, ?, ?)"""
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created successfully.'}, 201