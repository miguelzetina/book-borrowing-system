from django.urls import path

from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

from .routers import router
from ..autodiscover import autodiscover


autodiscover()

urlpatterns = router.urls + [
    path(
        'auth/token-refresh',
        refresh_jwt_token,
        name='auth-token-refresh'
    ),
    path(
        'auth/token-verify',
        verify_jwt_token,
        name='auth-token-verify'
    ),
]
