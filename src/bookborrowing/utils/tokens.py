# -*- coding: utf-8 -*-
from calendar import timegm
from datetime import datetime

from django.utils.six import text_type

from jwt import decode
from rest_framework_simplejwt.tokens import RefreshToken

def create_token(user):
    """
    Create token.
    """

    refresh = RefreshToken.for_user(user)

    token = text_type(refresh.access_token)

    return token
