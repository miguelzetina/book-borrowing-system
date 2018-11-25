# -*- coding: utf-8 -*-
from django.db.models import Q

from rest_condition import C

from rest_framework.response import Response

from bookborrowing.api.v1.routers import router
from bookborrowing.core.api.mixins import (
    ListModelMixin,
    RetrieveModelMixin
)
from bookborrowing.core.api.viewsets import GenericViewSet
from bookborrowing.users.models import User
from bookborrowing.users.permissions import (
    AdminPermission, SuperAdminPermission
)
from bookborrowing.users.serializers import UserSerializer
from bookborrowing.utils.schemas import CustomJSONAPISchema


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):

    serializer_class = UserSerializer
    list_serializer_class = UserSerializer
    retrieve_serializer_class = UserSerializer
    permission_classes = [C(SuperAdminPermission) | C(AdminPermission)]
    swagger_schema = CustomJSONAPISchema

    def get_queryset(self, *args, **kwargs):
        q = self.request.GET.get("q")
        users = User.objects.all()
        if q:
            users = users.filter(
                Q(name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(second_last_name__icontains=q) |
                Q(email__icontains=q)
            )

        return users.order_by("second_last_name", "last_name", "name")

    def list(self, request, *args, **kwargs):
        """
        Return list of users
        """
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Return a specific information about user
        """
        return super(UserViewSet, self).retrieve(
            request, *args, **kwargs
        )


router.register(
    r"users",
    UserViewSet,
    base_name="users",
)