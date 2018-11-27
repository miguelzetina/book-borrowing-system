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
from bookborrowing.books.models import Book
from bookborrowing.books.serializers import BookSerializer
from bookborrowing.users.permissions import (
    AdminPermission, SuperAdminPermission
)
from bookborrowing.utils.schemas import CustomJSONAPISchema


class BookViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):

    serializer_class = BookSerializer
    list_serializer_class = BookSerializer
    retrieve_serializer_class = BookSerializer
    permission_classes = [C(SuperAdminPermission) | C(AdminPermission)]
    swagger_schema = CustomJSONAPISchema

    def get_queryset(self, *args, **kwargs):
        q = self.request.GET.get("q")
        books = Book.objects.all()
        if q:
            books = books.filter(
                Q(author__first_name__icontains=q) |
                Q(author__last_name__icontains=q) |
                Q(genre__name__icontains=q) |
                Q(name__icontains=q)
            )

        return books.distinct().order_by('id')

    def list(self, request, *args, **kwargs):
        """
        Return list of books
        """
        return super(BookViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Return a specific information about book
        """
        return super(BookViewSet, self).retrieve(
            request, *args, **kwargs
        )


router.register(
    r"books",
    BookViewSet,
    base_name="books",
)