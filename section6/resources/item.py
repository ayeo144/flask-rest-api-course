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
        item = ItemModel.get_item_by_name(name)

        if item is not None:
            return item.to_json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        # we only want unique names in our item list, so check if item name already
        # exists in our 'items' list
        # Fail Fast!
        if ItemModel.get_item_by_name(name) is not None:
            # 400 is the status code for 'bad request'
            return {'message': f"An item with name '{name}' already exists"}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {'message': 'An error occurred inserting an item.'}, 500 # Internal Server Error

        return item.to_json(), 201 # HTTPS 201 is the code for creating something

    def delete(self, name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """DELETE FROM items WHERE name=?;"""
        cursor.execute(query, (name, ))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.get_item_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:

            try:
                updated_item.insert()
            except:
                return {'message': 'An error occurred inserting an item.'}, 500

        else:

            try:
                updated_item.update()
            except:
                return {'message': 'An error occurred updating an item.'}, 500

        return updated_item.to_json()


class ItemList(Resource):

    def get(self):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT * FROM items;"""
        result = cursor.execute(query)

        items = [{'name': row[0], 'price': row[1]} for row in result]

        connection.close()

        return {'items': items} # remember, 'items' is a list so we need to put it in a dictionary first