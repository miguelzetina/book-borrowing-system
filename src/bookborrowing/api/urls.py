from django.conf import settings
from django.urls import include, path, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework.permissions import AllowAny

urlpatterns = [
    path(
        'v1/', include(('bookborrowing.api.v1.urls', 'api'), namespace='v1')
    ),
]


if not settings.PRODUCTION:
    schema_view = get_schema_view(
        openapi.Info(
            title="Book Borrowing API",
            default_version='v1',
            description="API for Book Borrowing System",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="loefthur26@gmail.com"),
            license=openapi.License(name="BSD License"),
        ),
        validators=['flex'],
        public=True,
        permission_classes=(AllowAny,),
    )
    urlpatterns += [
        re_path(
            r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=None), name='schema-json'
        ),
        re_path(
            r'^swagger$',
            schema_view.with_ui('swagger', cache_timeout=None),
            name='schema-swagger-ui'
        ),
        re_path(
            r'^redoc$',
            schema_view.with_ui('redoc', cache_timeout=None),
            name='schema-redoc'
        ),
    ]
