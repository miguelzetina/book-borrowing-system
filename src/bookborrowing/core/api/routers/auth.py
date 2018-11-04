# -*- coding: utf-8 -*-
from rest_framework.routers import DynamicDetailRoute, Route
from rest_framework.routers import SimpleRouter as BaseRouter


class AuthenticationRouter(BaseRouter):
    """
    Custom router that shall be used to map authentication methods.
    """
    routes = [
        # Detail route
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'post': 'authenticate',
            },
            name='{basename}-authenticate',
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
