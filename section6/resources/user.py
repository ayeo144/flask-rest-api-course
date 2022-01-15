import sqlite3

from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):

        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user is not None:
            return {'message': 'Username already exists!'}, 400

        # because we are using a parser, data will only contain username and password keys
        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201