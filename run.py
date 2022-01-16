from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    """
    Creates all the tables in the database.
    """
    db.create_all()