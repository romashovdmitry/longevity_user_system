#default imports
from django.contrib import admin
from django.urls import path

# Swagger imports
from .yasg import urlpatterns as SWAG

# import router, viewsets
from api.router import router

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Swagger URLS
urlpatterns += SWAG
# router URLS
urlpatterns += router.urls

