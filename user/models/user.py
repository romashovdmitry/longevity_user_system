# Django imports
from typing import Any, Optional
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import UUIDField, EmailField, DateTimeField, ForeignKey, BigIntegerField, CharField, BooleanField
from django.db.models import Model, Index, CASCADE
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# Python imports
import uuid
from datetime import datetime, timedelta

# import JWT
import jwt

# import config data
from longevity.settings import SECRET_KEY

# import custom classes
from user.hash import hashing


class MyUserManager(UserManager):
    ''' Customize creating superuser for custom hashing passwords '''
    def create_superuser(self, email, password, **kwargs):

        original_password = password

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        user = super().create_superuser(email=email, **kwargs)
        user.password = hashing(password=original_password, user_id=user.id)
        user.save()


class MyUser(AbstractUser):
    ''' Custom user model '''
    first_name = last_name = None

    class Meta:

        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            Index(fields=['email'], name='user_email_index')
        ]

    objects = MyUserManager()

    id = UUIDField(default=uuid.uuid4, primary_key=True)
    email = EmailField(unique=True)
    created_at = DateTimeField(auto_now_add=True)

    def check_password(self, raw_password: str) -> bool:
        ''' redefine '''
        return hashing(password=raw_password, user_id=self.id) == self.password

    def save_new_password(self, new_password: str) -> None:
        ''' to renew password '''
        self.password = hashing(new_password, self.id)
        self.save()