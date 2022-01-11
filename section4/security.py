from werkzeug.security import safe_str_cmp 
from user import User


users = [

    User(1, 'bob', 'asdf')

]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    """
    This function authenticates a user with the username
    and password. 
    If the username exists and the given password matches the
    stored password for that user, then return the user object
    """
    # using .get instead of [''] lets us set a default return value (None)
    user = username_mapping.get(username, None)
    # this is a safe method for comparing strings accounting for string encoding
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    """
    payload is a flask-jwt object
    """
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)