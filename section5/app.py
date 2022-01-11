from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from user import UserRegister
from security import authenticate, identity
from item import Item, ItemList


app = Flask(__name__)
app.secret_key = 'alex'
api = Api(app)

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

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':

    app.run(port=5000, debug=True)