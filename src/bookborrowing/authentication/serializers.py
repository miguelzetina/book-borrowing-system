# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import AuthenticationFailed

from rest_framework_json_api import serializers

from bookborrowing.users.models import Role, User
from bookborrowing.utils.tokens import create_token


class LoginBackOfficeSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)

    password = serializers.CharField(
        max_length=20,
        required=True
    )

    def validate(self, validate_data):
        try:
            user = User.objects.get(email=validate_data["email"])
        except User.DoesNotExist:
            raise AuthenticationFailed()

        if not user.check_password(validate_data["password"]):
            raise AuthenticationFailed()

        return validate_data

    def get_user(self, data):
        """
        return user object
        """
        return User.objects.get(email__exact=data.get('email'))


class LoginBackOfficeResponseSerializer(serializers.ModelSerializer):
    """
    Serializer used to return the proper token, when the user was succesfully
    logged in.
    """
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('token', )

    def get_token(self, user):
        """
        Create JWT token.
        """
        return create_token(user)
