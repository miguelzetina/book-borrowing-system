# -*- coding: utf-8 -*-
from django.utils.six import text_type

from rest_framework_simplejwt.tokens import RefreshToken

def create_token(user):
    """
    Create token.
    """

    refresh = RefreshToken.for_user(user)

    token = text_type(refresh.access_token)

    return token