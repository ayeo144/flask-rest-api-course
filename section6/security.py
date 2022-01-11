from werkzeug.security import safe_str_cmp 
from resources.user import User


def authenticate(username, password):
    """
    This function authenticates a user with the username
    and password. 
    If the username exists and the given password matches the
    stored password for that user, then return the user object
    """
    # using .get instead of [''] lets us set a default return value (None)
    user = User.find_by_username(username)
    # this is a safe method for comparing strings accounting for string encoding
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    """
    payload is a flask-jwt object
    """
    user_id = payload['identity']
    return User.find_by_id(user_id)