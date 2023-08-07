# DRF imports
from rest_framework import serializers

# import models
from user.models.user import MyUser

# JWT imports
from rest_framework_simplejwt.tokens import RefreshToken

# for password check import
from django.contrib.auth.hashers import check_password

# import custom classes
from user.hash import hashing


class MyUserSerializer(serializers.ModelSerializer):
    ''' serializer for get objects of Product model'''

    email = serializers.EmailField(
        default=None,
        allow_blank=True,
        allow_null=True,
        trim_whitespace=True
    )
    username = serializers.CharField(
        max_length=128,
        allow_null=True,
        allow_blank=True,
        trim_whitespace=True
    )
    password = serializers.CharField(
        max_length=128,
        allow_null=True,
        trim_whitespace=True,
        required=True,
        label='Password'
    )

    class Meta:
        model = MyUser
        fields = [
            'username',
            'email',
            'password',
        ]

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')

        if not email and not username:
            raise serializers.ValidationError("At least one of 'email' or 'username' is required.")

        if not password:
            raise serializers.ValidationError(
                'Password is required field'
            )

        return attrs


class AuthSerializer(MyUserSerializer):

    def validate(self, attrs):
        ''' validate password and email '''
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')

        user = self.instance

        if user.check_password(password):
            refresh_token = RefreshToken.for_user(user)
            return {
                'access token': f'Bearer {str(refresh_token.access_token)}',
                'refresh token': str(refresh_token)
            }
        raise serializers.ValidationError(
            'Incorrect password'
        )

