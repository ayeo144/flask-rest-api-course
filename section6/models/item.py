import sqlite3

"""
We now have an ItemModel class which contains the properties of
an item (name and price), however it also has several methods
such as insert/update/get. Do these methods really belong in this class?
"""

class ItemModel:

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def to_json(self):
        return {'name': self.name, 'price': self.price}

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

    @classmethod
    def update_item(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """UPDATE items SET price=? WHERE name=?;"""
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()