# -*- coding: utf-8 -*-
from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.inspectors.base import (
    FieldInspector, NotHandled, PaginatorInspector, ViewInspector
)

from rest_framework.fields import DateTimeField, EmailField, IntegerField
from rest_framework.pagination import LimitOffsetPagination

from rest_framework_json_api import serializers
from rest_framework_json_api.utils import (
    get_related_resource_type, get_resource_type_from_serializer
)


class ResourceRelatedFieldInspector(ViewInspector):

    def field_to_swagger_object(
            self, field, swagger_object_type, use_references, **kwargs
    ):
        if isinstance(field, serializers.ResourceRelatedField):
            return None

        return NotHandled


class ModelSerializerInspector(FieldInspector):

    def process_result(self, result, method_name, obj, **kwargs):
        if (
            isinstance(obj, serializers.ModelSerializer) and
            method_name == 'field_to_swagger_object'
        ):
            model_response = self.formatted_model_result(result, obj)
            if obj.parent is None and self.view.action != 'list':
                # It will be top level object not in list, decorate with data
                return self.decorate_with_data(model_response)

            return model_response

        return result

    def generate_relationships(self, obj):
        relationships_properties = []
        for field in obj.fields.values():
            if isinstance(field, serializers.ResourceRelatedField):
                relationships_properties.append(
                    self.generate_relationship(field)
                )
        if relationships_properties:
            return openapi.Schema(
                title='Relationships of object',
                type=openapi.TYPE_OBJECT,
                properties=OrderedDict(relationships_properties),
            )

    def generate_relationship(self, field):
        field_schema = openapi.Schema(
            title='Relationship object',
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict((
                ('type', openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title='Type of related object',
                    enum=[get_related_resource_type(field)]
                )),
                ('id', openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title='ID of related object',
                ))
            ))
        )
        return field.field_name, self.decorate_with_data(field_schema)

    def generate_attributes_without_relationship(self, obj):
        properties = OrderedDict([])
        for field in obj.fields.values():
            if not isinstance(
                field, serializers.ResourceRelatedField
            ) and field.field_name != "id":

                format_object = None
                type_object = openapi.TYPE_STRING

                if isinstance(field, IntegerField):
                    type_object = openapi.TYPE_INTEGER
                    format_object = openapi.FORMAT_INT32

                if isinstance(field, EmailField):
                    format_object = openapi.FORMAT_EMAIL

                if isinstance(field, DateTimeField):
                    format_object = openapi.FORMAT_DATETIME

                if "number" in field.field_name:
                    type_object = openapi.TYPE_INTEGER
                    format_object = openapi.FORMAT_INT32

                properties.update({field.field_name: openapi.Schema(
                    type=type_object,
                    format=format_object
                )})

        if properties:
            return openapi.Schema(
                title='Relationships of object',
                type=openapi.TYPE_OBJECT,
                properties=OrderedDict(properties),
            )

    def formatted_model_result(self, result, obj):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['properties'],
            properties=OrderedDict((
                ('type', openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=[get_resource_type_from_serializer(obj)],
                    title='Type of related object',
                )),
                ('id', openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title='ID of related object',
                    read_only=True
                )),
                (
                    'attributes',
                    self.generate_attributes_without_relationship(obj)
                ),
                ('relationships', self.generate_relationships(obj))
            ))
        )

    def decorate_with_data(self, result):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties=OrderedDict((
                ('data', result),
            ))
        )


class ResponsePaginationInspector(PaginatorInspector):

    def get_paginator_parameters(self, paginator):
        return [
            openapi.Parameter(
                'page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            ),
        ]

    def get_paginated_response(self, paginator, response_schema):
        paged_schema = None
        if not isinstance(paginator, LimitOffsetPagination):
            paged_schema = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=OrderedDict((
                    ('links', self.generate_links()),
                    ('data', response_schema),
                    ('meta', self.generate_meta())
                )),
                required=['data']
            )

        return paged_schema

    def generate_links(self):
        return openapi.Schema(
            title='Links',
            type=openapi.TYPE_OBJECT,
            required=['first', 'last'],
            properties=OrderedDict((
                ('first', openapi.Schema(
                    type=openapi.TYPE_STRING, title='Link to first object',
                    read_only=True, format=openapi.FORMAT_URI
                )),
                ('last', openapi.Schema(
                    type=openapi.TYPE_STRING, title='Link to last object',
                    read_only=True, format=openapi.FORMAT_URI
                )),
                ('next', openapi.Schema(
                    type=openapi.TYPE_STRING, title='Link to next object',
                    read_only=True, format=openapi.FORMAT_URI
                )),
                ('prev', openapi.Schema(
                    type=openapi.TYPE_STRING, title='Link to prev object',
                    read_only=True, format=openapi.FORMAT_URI
                ))
            ))
        )

    def generate_meta(self):
        return openapi.Schema(
            title='Meta of result with pagination count',
            type=openapi.TYPE_OBJECT,
            required=['count'],
            properties=OrderedDict((
                ('count', openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    title='Number of results on page',
                )),
            ))
        )
