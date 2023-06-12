import hashlib
import secrets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken


def generate_code(number):
    # Generate a random string
    random_string = secrets.token_hex(number)
    return random_string


def authenticate_token(token):
    try:
        decoded_token = AccessToken(token)
        decoded_token.verify()
        user = JWTAuthentication().get_user(decoded_token)
        return True, user
    except:
        return False, None
