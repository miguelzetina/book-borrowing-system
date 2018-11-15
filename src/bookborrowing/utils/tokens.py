# -*- coding: utf-8 -*-
from calendar import timegm
from datetime import datetime

from jwt import decode

from rest_framework_jwt.settings import api_settings


def jwt_decode_handler(token):
    """
    Decode token for user
    """
    options = {
        'verify_exp': False,
    }

    return decode(
        token,
        api_settings.JWT_SECRET_KEY,
        api_settings.JWT_VERIFY,
        options=options,
        leeway=api_settings.JWT_LEEWAY,
        audience=api_settings.JWT_AUDIENCE,
        issuer=api_settings.JWT_ISSUER,
        algorithms=[api_settings.JWT_ALGORITHM]
    )


def create_token(user):
    """
    Create token.
    """
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    # Return value
    token = jwt_encode_handler(payload)
    return token
