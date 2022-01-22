from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager


from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# if Flask JWT raies an error, then Flask will propagate the correct errors
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose' # app.config['JWT_SECRET_KEY']
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)  # no longer creating /auth

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    """
    Whenever a JWT is created, this function will
    run to see if any additional data should be added
    to the token.
    """
    # First user created is an admin user
    if identity == 1: # instead of hard-coding, this should be in database or config
        return {'is_admin': True}
    return {'is_admin': False}



api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
