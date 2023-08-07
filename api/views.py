# DRF imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import UserRateThrottle

# import models
from user.models.user import MyUser

# serializers imports
from api.serializers import MyUserSerializer, UpdateSerializer

# JWT imports
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

# import custom classes
from user.hash import hashing
from api.permissions import CurrentUserPermission
from api.paginators import UsersPagination


class UserViewSet(ModelViewSet):
    ''' class for API processing users data '''
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [CurrentUserPermission]
    http_method_names = ['get', 'delete', 'put', 'post']
    pagination_class = UsersPagination

    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def update_helper(self, user, request):
        ''' helper for update endpoints '''
        serializer = UpdateSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            if 'password' in validated_data.keys():
                validated_data['password'] = hashing(
                    validated_data['password'],
                    user.id
                )
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        ''' registrate new user '''
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
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
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

    def update(self, request, *args, **kwargs) -> Response:
        ''' update user info '''
        user = self.get_object()
        serializer_data = self.update_helper(
            user=user,
            request=request
        )
        return Response(serializer_data.data, status=HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_me(self, request):
        ''' user get info about himself '''
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def delete_me(self, request):
        ''' user deletes himself '''
        user = request.user
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['put'])
    def update_me(self, request):
        ''' user update info about himself '''
        user = request.user
        data = self.update_helper(
            user=user,
            request=request
        )
        return Response(data)

class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [UserRateThrottle]