# -*- coding: utf-8 -*-
from rest_framework_nested.routers import NestedSimpleRouter

from .auth import AuthenticationRouter
from .simple import SimpleRouter
from .single import SingleObjectRouter


class DefaultRouter(SimpleRouter):
    """
    Default router that provides shortcuts to register single object viewsets.
    """
    _single_object_registry = []
    _nested_object_registry = []

    def register(self, prefix, viewset, base_name=None, router_class=None):
        """
        Append the given viewset to the proper registry.
        """
        if base_name is None:
            base_name = self.get_default_base_name(viewset)

        if router_class is not None:
            kwargs = {'trailing_slash': bool(self.trailing_slash)}
            single_object_router_classes = (
                AuthenticationRouter, SingleObjectRouter)

            if issubclass(router_class, single_object_router_classes):
                router = router_class(**kwargs)
                router.register(prefix, viewset, base_name=base_name)
                self._single_object_registry.append(router)

        else:
            self.registry.append((prefix, viewset, base_name))

    def register_nested(self, parent_prefix, prefix, viewset,
                        base_name=None, parent_lookup_name=None,
                        depth_level=1):
        """
        Register a nested viewset wihtout worrying of instantiate a nested
        router for registry.
        """
        kwargs = {
            'trailing_slash': bool(self.trailing_slash)
        }

        if parent_lookup_name is not None:
            kwargs.update(lookup=parent_lookup_name)

        # Section for the depth of the route and add more routes

        if depth_level > 1:
            routers = filter(
                lambda r: (r._depth_level == (depth_level - 1)) and
                r._nested_prefix == parent_prefix,
                self._nested_object_registry
            )

            try:
                parent_router = routers.next()
            except StopIteration:
                raise RuntimeError('parent registered resource not found')

        else:
            parent_router = self

        nested_router = NestedSimpleRouter(
            parent_router,
            parent_prefix,
            **kwargs
        )

        nested_router._nested_prefix = prefix
        nested_router._depth_level = depth_level
        nested_router.register(prefix, viewset, base_name)
        self._nested_object_registry.append(nested_router)

    def get_urls(self):
        """
        Generate the list of URL patterns including the registered single
        object routers urls.
        """
        base_urls = super(SimpleRouter, self).get_urls()
        single_urls = sum([r.urls for r in self._single_object_registry], [])
        nested_urls = sum([r.urls for r in self._nested_object_registry], [])

        return base_urls + single_urls + nested_urls
