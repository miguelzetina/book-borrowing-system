# -*- coding: utf-8 -*-
from rest_framework.reverse import reverse

from rest_framework_json_api import serializers


class AbsoluteUriMixin(object):
    """
    Simple mixin that brings a method for returning a fully qualified
    absolute uri.
    """

    def build_absolute_uri(self, uri):
        """
        Return a fully qualified absolute url for the given uri.
        """
        request = self.context.get('request', None)

        return (request.build_absolute_uri(uri) if
                request is not None else uri)


class DynamicFieldsMixin(object):
    """
    Simple mixin that allows a serializer to be initialized specifying the
    fields to be serialized.
    Note that if fields are not defined or is explicit assigned to an empty
    iterable or a falsy value, then the serializer will ignore this and will
    have all the fields declared at load time.
    Example:

        >>> from rest_framework import serializers
        ...
        >>> class MySerializer(DynamicFieldsMixin, serializers.Serializer):
        ...     field1 = serializers.IntegerField()
        ...     field2 = serializers.IntegerField()
        ...     field3 = serializers.IntegerField()
        ...     class Meta:
        ...         fields = ['field1', 'field2', 'field3']
        ...
        >>> obj = {'field1': 1, 'field2': 2, 'field3': 3}
        >>> serializer = MySerializer(obj, fields=['field1', 'field3'])
        ...
        >>> serializer.data == {'field1': 1, 'field3': 3}
        True
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', [])

        super(DynamicFieldsMixin, self).__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())

            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ParentObjectMixin(object):
    """
    Simple mixin to extends a serializer __init__ method to allow an optional
    parenrt_object parameter. Useful for nested serializers whose need to
    access a parent resource.
    """

    def __init__(self, *args, **kwargs):
        self.parent_object = kwargs.pop('parent_object', None)

        super(ParentObjectMixin, self).__init__(*args, **kwargs)


class ModelSerializer(DynamicFieldsMixin, AbsoluteUriMixin,
                      serializers.ModelSerializer):
    """
    Simple serializer for model objects.
    """
    lookup_field = 'pk'
    api_version = 'v1'
    custom_lookup_fields = None
    custom_base_name = None
    resource_uri = serializers.SerializerMethodField()

    def clean_lookup_fields(self):
        """
        Returns a list with the properties that will be lookup by
        get_resource_uri function
        """
        custom_lookup_fields = {}
        for key, string_values in self.custom_lookup_fields.iteritems():
            values = string_values.split('__')
            custom_lookup_fields[key] = values

        return custom_lookup_fields

    def get_resource_uri(self, obj):
        """
        Return the uri of the given object.
        """
        base_name = getattr(
            self, 'resource_view_name',
            self.Meta.model._meta.model_name
        )
        if self.custom_base_name:
            base_name = self.custom_base_name

        url = 'api:%s:%s-detail' % (
            self.api_version,
            base_name
        )

        request = self.context.get('request')
        kwargs = {self.lookup_field: getattr(obj, self.lookup_field)}

        #
        # Using custom lookup fields if any.
        #
        if self.custom_lookup_fields is not None:
            kwargs = {}
            lookup_fields = self.clean_lookup_fields()

            for key, values in lookup_fields.iteritems():
                current_value = obj
                for field in values:
                    current_value = getattr(current_value, field)

                kwargs[key] = current_value

        return reverse(
            url,
            request=request,
            kwargs=kwargs
        )
