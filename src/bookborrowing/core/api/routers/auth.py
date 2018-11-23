# -*- coding: utf-8 -*-
from rest_framework.routers import DynamicRoute, Route
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
            detail=False,
            name='{basename}-authenticate',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}$',
            name='{basename}-{ur_name}',
            detail=True,
            initkwargs={}
        ),
    ]
