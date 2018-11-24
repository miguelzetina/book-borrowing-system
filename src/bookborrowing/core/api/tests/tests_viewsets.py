# -*- coding: utf-8 -*-
from django.utils.six import text_type

from rest_framework_simplejwt.tokens import RefreshToken

from bookborrowing.users.models import User


class ApiTestMixin(object):
    """
    Common operations for API testing
    """

    def create_token(user):
        """
        Create token.
        """
        refresh = RefreshToken.for_user(user)
        token = text_type(refresh.access_token)
        return token

    def create_superuser(self):
        user = User.objects.create_superuser(
            email='superadmin@mail.com'
        )
        user.set_password('password')
        user.save()
        return user