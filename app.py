from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from security import authenticate, identity
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # we have told the app we have two models coming from our database
app.secret_key = 'alex'
api = Api(app)

# @app.before_first_request
# def create_tables():
#     """
#     Creates all the tables in the database.
#     """
#     db.create_all()

# when we initialise the JWT class, we use our functions for
# authentication and getting user ID's
# This creates a new endpoint for our API, /auth

# /auth, when we call this we send a username and password, which gets sent
# to out authenticate function
# if authentication is succesful, the endpoint returns a JW token
# this token is then sent along with any more requests, and the identity function
# uses it to get the user ID
# if it can do this, then the user was authenticated and the token is valid
jwt = JWT(app, authenticate, identity) 

"""
With Flask-Restful we don't need to use flask.jsonify, we can
just return a dictionary instead.
"""

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':

    db.init_app(app)
    app.run(port=5000, debug=True)