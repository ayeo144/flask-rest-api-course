import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True)

    @staticmethod
    def items_name_filter(name):
        return filter(lambda x: x['name'] == name, items)


    @classmethod
    def get_item_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT * FROM items WHERE name=?;"""
        result = cursor.execute(query, (name, ))
        row = result.fetchone()

        connection.close()

        if row is not None:
            return {'item': {'name': row[0], 'price': row[1]}}


    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """INSERT INTO items VALUES (?, ?);"""
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()


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
        item = self.get_item_by_name(name)

        if item is not None:
            return item
        return {'message': 'Item not found'}, 404


    def post(self, name):
        # we only want unique names in our item list, so check if item name already
        # exists in our 'items' list
        # Fail Fast!
        if self.get_item_by_name(name) is not None:
            # 400 is the status code for 'bad request'
            return {'message': f"An item with name '{name}' already exists"}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        try:
            self.insert_item(item)
        except:
            return {'message': 'An error occurred inserting an item.'}, 500 # Internal Server Error

        return item, 201 # HTTPS 201 is the code for creating something


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

        item = self.get_item_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:

            try:
                self.insert_item(updated_item)
            except:
                return {'message': 'An error occurred inserting an item.'}, 500

        else:

            try:
                self.update_item(updated_item)
            except:
                return {'message': 'An error occurred updating an item.'}, 500

        return updated_item


    @classmethod
    def update_item(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """UPDATE items SET price=? WHERE name=?;"""
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()



class ItemList(Resource):

    def get(self):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT * FROM items;"""
        result = cursor.execute(query)

        items = [{'name': row[0], 'price': row[1]} for row in result]

        connection.close()

        return {'items': items} # remember, 'items' is a list so we need to put it in a dictionary first