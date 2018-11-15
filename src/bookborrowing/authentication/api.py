# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from bookborrowing.api.v1.routers import router
from bookborrowing.authentication.serializers import (
    LoginBackOfficeResponseSerializer,
    LoginBackOfficeSerializer
)
from bookborrowing.core.api.viewsets import GenericViewSet
from bookborrowing.utils.schemas import CustomJSONAPISchema


class LoginAPIView(GenericViewSet):
    """
    Login
    """

    resource_name = ''
    serializer_class = LoginBackOfficeSerializer
    local_serializer_class = LoginBackOfficeSerializer
    permission_classes = (AllowAny, )
    swagger_schema = CustomJSONAPISchema

    @swagger_auto_schema(
        responses={200: LoginBackOfficeResponseSerializer},
        request_body=LoginBackOfficeSerializer
    )
    @list_route(methods=['POST'])
    def local(self, request, *args, **kwargs):
        """
        User login in the backoffice.
        ---
        Response 200
        ---
            {
                'data': {
                    'type': 'login_backoffice',
                    'id': <string>,
                    'attributes': {
                        'token': <string>,
                    }
                }
            }

        """
        self.resource_name = 'login_backoffice'
        login_serializer = LoginBackOfficeSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        user = login_serializer.get_user(data=request.data)
        response_serializer = LoginBackOfficeResponseSerializer(user)
        return Response(response_serializer.data)


router.register(
    r'auth',
    LoginAPIView,
    base_name="auth",
)
