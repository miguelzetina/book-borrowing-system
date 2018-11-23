# -*- coding: utf-8 -*-
from rest_framework.routers import DynamicRoute, Route
from rest_framework.routers import SimpleRouter as BaseRouter


class SimpleRouter(BaseRouter):
    """
    Custom Router that maps viewset methods to its methodnamehyphen variant.

    For example:
        Method do_some_stuff will be translated to url resource/do-some-stuff
    """
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            detail=False,
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes.
        # Generated using @action decorator
        # on methods of the viewset with param
        # detail=False.
        DynamicRoute(
            url=r'^{prefix}/{url_path}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            detail=True,
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes.
        # Generated using @action decorator
        # on methods of the viewset with param
        # detail=True.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]
