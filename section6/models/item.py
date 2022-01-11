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
        """
        Keep this as a classmethod that can now return an
        instance of ItemModel.

        'cls' calls the __init__ method of whatever class it
        is a classmethod of
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT * FROM items WHERE name=?;"""
        result = cursor.execute(query, (name, ))
        row = result.fetchone()

        connection.close()

        if row is not None:
            name, price = row # unpack into name and price
            return cls(name, price)

    def insert(self):
        """
        Update to use self and work in instance of ItemModel with
        name and price atributes. So we can call 
                >> item = ItemModel(name, price)
                >> item.insert()
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """INSERT INTO items VALUES (?, ?);"""
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()

    def update(self):
        """
        Similar logic to self.insert()
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """UPDATE items SET price=? WHERE name=?;"""
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()