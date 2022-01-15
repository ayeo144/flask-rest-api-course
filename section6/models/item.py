from db import db

"""
We now have an ItemModel class which contains the properties of
an item (name and price), however it also has several methods
such as insert/update/get. Do these methods really belong in this class?
"""

class ItemModel(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # Every ItemModel has a 'store' property which is the store that matches the 'store_id'
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    # Now using Flask-SQLAlchemy, the name and price values from the
    # database are put into the __init__ method below to create an object

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def to_json(self):
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self) # because we have extended this class with db.Model we can just add self as a record
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()