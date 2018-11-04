# -*- coding: utf-8 -*-
from rest_framework.generics import GenericAPIView as BaseGenericAPIView
from rest_framework.viewsets import GenericViewSet as BaseGenericViewSet


class GenericViewSet(BaseGenericViewSet):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """

    def get_serializer_class(self, action=None):
        """
        Return the serializer class depending on request method.

        Attribute of proper serializer should be defined.
        """
        if action is not None:
            return getattr(self, '%s_serializer_class' % action)
        else:
            return super(GenericViewSet, self).get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        """
        Returns the serializer instance that should be used to the
        given action.

        If any action was given, returns the serializer_class
        """
        action = kwargs.pop('action', None)

        serializer_class = self.get_serializer_class(action)

        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class GenericAPIView(BaseGenericAPIView):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """

    def get_serializer_class(self, action=None):
        """
        Return the serializer class depending on request method.

        Attribute of proper serializer should be defined.
        """
        if action is not None:
            return getattr(self, '%s_serializer_class' % action)
        else:
            return super(GenericViewSet, self).get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        """
        Returns the serializer instance that should be used to the
        given action.

        If any action was given, returns the serializer_class
        """
        action = kwargs.pop('action', None)

        serializer_class = self.get_serializer_class(action)

        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
