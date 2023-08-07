# DRF imports
from rest_framework import serializers

# import models
from user.models.user import MyUser

# JWT imports
from rest_framework_simplejwt.tokens import RefreshToken


# import custm classes
from api.validation import ValidateFieldsHelper

class MyUserSerializer(serializers.ModelSerializer):
    ''' serializer for get objects of Product model'''

    email = serializers.EmailField(
        default=None,
        allow_blank=True,
        allow_null=True,
        trim_whitespace=True,
        label='Email'
    )
    username = serializers.CharField(
        max_length=128,
        allow_null=True,
        allow_blank=True,
        trim_whitespace=True,
        label='Username'
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

        ValidateFieldsHelper(
            email=email,
            username=username,
            password=password
        ).validate_all()

        return attrs


class AuthSerializer(MyUserSerializer):

    def validate(self, attrs):
        ''' validate password and email '''
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')

        validation = ValidateFieldsHelper(
            email=email,
            username=username,
            password=password
        )
        validation.validate_required()
        validation.validate_required_email_user()
        validation.validate_email()

        if username:
            user = MyUser.objects.filter(username=username).first()
            if not user:
                raise serializers.ValidationError(
                    "API didn't find suitable user, "
                    "try search by email or another username"
                )

        else:
            user = MyUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError(
                    "API didn't find suitable user, "
                    "try search by username or another email"
                )
        if user.check_password(password):
            refresh_token = RefreshToken.for_user(user)
            return {
                'access token': f'Bearer {str(refresh_token.access_token)}',
                'refresh token': str(refresh_token)
            }
        raise serializers.ValidationError(
            'Incorrect password'
        )


class UpdateSerializer(MyUserSerializer):
    ''' serializer for update user info '''
    def validate(self, attrs):
        '''
        just to clean up validate method
        from parent class MyUserSerializer
        '''
        email = attrs.get('email')
        if email:
            ValidateFieldsHelper(email=email).validate_email()
        return attrs