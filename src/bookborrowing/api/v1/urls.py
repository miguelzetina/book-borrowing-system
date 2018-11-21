from django.urls import path, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .routers import router
from ..autodiscover import autodiscover


autodiscover()

urlpatterns = router.urls + [
    re_path(
        '^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    re_path(
        '^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'
    ),
]
