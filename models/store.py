from db import db

"""
db.relationship tells us which tables have relationships wit eachother

the ForeignKey is used to define the nature of that relationship

We have a one-to-many relationship for store to items 
"""


class StoreModel(db.Model):

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # a back reference allows a store to see which items are in the items tables for a given store

    # this variable will be a list of ItemModels
    # however if we use lazy='dynamic', it will not create a list of objects as this could be
    # an expensive operation if we have lots of items in a store
    items = db.relationship('ItemModel', lazy='dynamic') 

    # Now using Flask-SQLAlchemy, the name and price values from the
    # database are put into the __init__ method below to create an object

    def __init__(self, name):
        self.name = name

    def to_json(self):
        # because we are using lazy='dynamic', self.items becomes a query builder and we 
        # have to use self.items.all() to actually query the database and get all the items
        # for a store
        return {'name': self.name, 'items': [item.to_json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self) # because we have extended this class with db.Model we can just add self as a record
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()