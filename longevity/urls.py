#default imports
from django.contrib import admin
from django.urls import path

# Swagger imports
from .yasg import urlpatterns as SWAG

# import router, viewsets
from api.router import router

# JWT imports
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # default URL
    path('admin/', admin.site.urls),
    # JWT URLs
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view())
]

# Swagger URLS
urlpatterns += SWAG
# router URLS
urlpatterns += router.urls

