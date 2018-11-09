# -*- coding: utf-8 -*-
from rest_framework_jwt.settings import api_settings

from bookborrowing.users.models import User


class ApiTestMixin(object):
    """
    Common operations for API testing
    """

    def create_token(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        return 'JWT {0}'.format(jwt_encode_handler(payload))

    def create_admin(self):
        user = User.objects.create(
            email='admin@mail.com', is_active=True, role_id=1
        )
        user.set_password('password')
        user.save()
        return user

    def create_superadmin(self):
        user = User.objects.create(
            email='superadmin@mail.com', is_active=True, role_id=3
        )
        user.set_password('password')
        user.save()
        return user

    def create_app(self):
        user = User.objects.create(
            email='app@mail.com', is_active=True, role_id=2
        )
        user.set_password('password')
        user.save()
        return user
