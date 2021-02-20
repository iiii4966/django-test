from functools import wraps

import jwt
from django.http import HttpResponse
from jwt import DecodeError, ExpiredSignatureError
from django.conf import settings

from accounts.models import User


class JWTAuthenticator:
    """
    TODO: to decorator
    """

    AUTH_HEADER_NAME = 'Authorization'
    TOKEN_PREFIX = 'Bearer'
    USER_ID_CLAIM = 'user_id'
    USER_ID_FIELD = 'id'
    HASH_ALGORITHEM = 'HS256'

    @classmethod
    def authenticate(cls, request):
        header = cls.get_header(request)
        if header is None:
            return False

        raw_token = cls.get_raw_token(header)
        if raw_token is None:
            return False

        claim = cls.decode_token(raw_token)
        if claim is None:
            return False

        user = cls.get_user(claim)
        if user is None:
            return False

        setattr(request, 'user', user)
        return True

    @classmethod
    def get_header(cls, request):
        return request.META.get(cls.AUTH_HEADER_NAME)

    @staticmethod
    def get_raw_token(header):
        parts = header.split(" ")
        if len(parts) != 2:
            return None
        return parts[1]

    @classmethod
    def decode_token(cls, raw_token):
        try:
            return jwt.decode(raw_token.encode(), settings.SECRET_KEY, cls.HASH_ALGORITHEM)
        except (DecodeError, ExpiredSignatureError):
            return None

    @classmethod
    def encode_token(cls, **kwargs):
        user = kwargs.get('user')
        if isinstance(kwargs.get('user'), User):
            token = jwt.encode({'user_id': user.id}, settings.SECRET_KEY)
        else:
            token = jwt.encode(kwargs, settings.SECRET_KEY)
        return f"{cls.TOKEN_PREFIX} {token}"

    @classmethod
    def get_user(cls, claim):
        user_id = claim.get(cls.USER_ID_CLAIM)
        if user_id is None:
            return None
        return User.objects.filter(**{cls.USER_ID_FIELD: user_id}).first()


def jwt_authenticate(view_func):

    @wraps(view_func)
    def wrapper(view_obj, request, *args, **kwargs):
        if JWTAuthenticator.authenticate(request):
            return view_func(view_obj, request, *args, **kwargs)
        return HttpResponse(status=401, content="Not Authenticated")

    return wrapper
