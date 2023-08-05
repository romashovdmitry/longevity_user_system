# DRF imports
from rest_framework import serializers

# import models
from user.models.user import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    ''' serializer for get objects of Product model'''

    class Meta:
        model = MyUser
        fields = '__all__'
