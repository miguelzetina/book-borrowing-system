# -*- coding: utf-8 -*-
from rest_framework.routers import DynamicDetailRoute, Route
from rest_framework.routers import SimpleRouter as BaseRouter


class SingleObjectRouter(BaseRouter):
    """
    Custom router for compose urls for single object viewsets.
    """
    routes = [
        # Detail route
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicDetailRoute(
            url=r'^{prefix}/{methodnamehyphen}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]
