# DRF imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.filters import SearchFilter

# import models
from user.models.user import MyUser

# serializers imports
from api.serializers import MyUserSerializer, AuthSerializer

# JWT imports
from rest_framework_simplejwt.tokens import RefreshToken

# import custom classes
from api.permissions import CurrentUserPermission
from user.hash import hashing


class MyUserViewSet(ModelViewSet):
    ''' process data  '''
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'list']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update', 'retrieve', 'destroy']:
            permission_classes = [CurrentUserPermission]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        ''' registrate new user '''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        validated_data = serializer.validated_data
        instance = serializer.save()
        instance.password = hashing(
            validated_data['password'],
            instance.id
        )
        instance.save()
        refresh_token = RefreshToken.for_user(instance)

        response_data = {
            "user": serializer.validated_data,
            'access token': f'Bearer {str(refresh_token.access_token)}',
            'refresh token': str(refresh_token)
        }
        return Response(response_data, status=HTTP_201_CREATED)        

    def update(self, request, *args, **kwargs) -> Response:
        ''' update user info '''
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['password'] = hashing(
            validated_data['password'], 
            instance.id
        )
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
