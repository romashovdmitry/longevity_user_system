# DRF imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# import models
from user.models.user import MyUser

# serializers imports
from api.serializers import MyUserSerializer


class MyUserViewSet(ModelViewSet):
    ''' process data  '''
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    http_method_names = ['get', 'post', 'update', 'delete']
    permission_classes = [AllowAny]
