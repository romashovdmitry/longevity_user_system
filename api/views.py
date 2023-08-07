# DRF imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

# import models
from user.models.user import MyUser

# serializers imports
from api.serializers import MyUserSerializer, AuthSerializer

# JWT imports
from rest_framework_simplejwt.tokens import AccessToken

# import custom classes
from api.permissions import CurrentUserPermission
from user.hash import hashing


class MyUserViewSet(ModelViewSet):
    ''' process data  '''
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):

        if self.action == ['create', 'list']:
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
        user = serializer.create(serializer.validated_data)
        user = serializer.save()
        access_token = AccessToken.for_user(user)

        response_data = {
            "user": serializer.validated_data,
            "token": f'Bearer {str(access_token)}'
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

    @action(detail=False, methods=['post'], serializer_class=AuthSerializer)
    def authorize_user(self, request) -> Response:
        ''' authorize on API '''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=HTTP_200_OK)
