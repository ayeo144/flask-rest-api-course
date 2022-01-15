import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True)

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
        item = ItemModel.find_by_name(name)

        if item is not None:
            return item.to_json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        # we only want unique names in our item list, so check if item name already
        # exists in our 'items' list
        # Fail Fast!
        if ItemModel.find_by_name(name) is not None:
            # 400 is the status code for 'bad request'
            return {'message': f"An item with name '{name}' already exists"}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting an item.'}, 500 # Internal Server Error

        return item.to_json(), 201 # HTTPS 201 is the code for creating something

    def delete(self, name):
        item = ItemModel.find_by_name()
        if item is not None:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:

            item = ItemModel(name, data['price'])
            
        else:

            item.price = data['price']

        item.save_to_db() # if the price has changed, SQLAlchemy will update, if it doesn't exist it will add a new record

        return item.to_json()


class ItemList(Resource):

    def get(self):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT * FROM items;"""
        result = cursor.execute(query)

        items = [{'name': row[0], 'price': row[1]} for row in result]

        connection.close()

        return {'items': items} # remember, 'items' is a list so we need to put it in a dictionary first