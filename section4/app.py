from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity


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


items = []

"""
With Flask-Restful we don't need to use flask.jsonify, we can
just return a dictionary instead.
"""

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True)

    def items_name_filter(self, name):
        return filter(lambda x: x['name'] == name, items)


    @jwt_required()
    def get(self, name):
        """
        # filter function iterates through a list of
        # objects and applies a filtering function to
        # each object, returning the object which matches
        # the filter

        # in our case the filter function should only find
        # one item in the list, we can call 'next' to return 
        # the first object from the filter
        # if 'next' doesn't find an item, return None
        """

        item = next(self.items_name_filter(name), None)

        # return tuple, the JSON item and the HTTP status code
        status_code = 200 if item is not None else 404

        return {'item': item}, status_code


    def post(self, name):
        # we only want unique names in our item list, so check if item name already
        # exists in our 'items' list
        # Fail Fast!
        if next(self.items_name_filter(name), None) is not None:
            # 400 is the status code for 'bad request'
            return {'message': f"An item with name '{name}' already exists"}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 # HTTPS 201 is the code for creating something


    def delete(self, name):
        # call this to ensure we use the 'global' items variable defined outside this method
        global items
        # overwrite the items variable to exclude the item with name we want to delete
        items = list(self.items_name_filter(name))
        return {'message': 'Item deleted'}


    def put(self, name):
        data = Item.parser.parse_args()

        item = next(self.items_name_filter(name), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item




class ItemList(Resource):

    def get(self):
        return {'items': items} # remember, 'items' is a list so we need to put it in a dictionary first


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


if __name__ == '__main__':

    app.run(port=5000, debug=True)