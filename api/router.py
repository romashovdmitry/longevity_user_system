from rest_framework.routers import DefaultRouter

from api.views import MyUserViewSet

router = DefaultRouter()
router.register(r'v1/users', MyUserViewSet, basename='users')