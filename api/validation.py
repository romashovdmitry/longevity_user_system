# DRF imports
from rest_framework import serializers

# import models
from user.models.user import MyUser

# Python imports
import re

# Django imports
from django.core.validators import validate_email

class ValidateFieldsHelper:
    ''' validate helper class '''

    def __init__(self, email=None, username=None, password=None):
        ''' usual initiliaze instance '''
        self.email = email
        self.username = username
        self.password = password

    @staticmethod
    def validate_substring(str1: str, str2: str) -> bool:
        ''' validate username substring in password '''
        len1 = len(str1)
        len2 = len(str2)
        max_length = 0

        for i in range(len1):
            for j in range(len2):
                length = 0
                while i + length < len1 and j + length < len2 and str1[i + length] == str2[j + length]:
                    length += 1
                max_length = max(max_length, length)
        print(max_length)
        print(len2 * 0.75)
        print(max_length >= (len2 * 0.75))
        if max_length < (len2 * 0.75):
            return True
        return False

    @staticmethod
    def count_algo_helper(string: str) -> bool:
        ''' to count repeating symbols '''
        char_count = {}  # Словарь для подсчета символов
        max_count = 0    # Максимальное количество повторений
        max_chars = []   # Символы с максимальным количеством повторений
        stop_counting = len(string) // 3

        while max_count < stop_counting:
            for char in string:
                if char in char_count:
                    char_count[char] += 1
                else:
                    char_count[char] = 1

                if char_count[char] > max_count:
                    max_count = char_count[char]
                    max_chars = [char]
                elif char_count[char] == max_count:
                    max_chars.append(char)
            return True
        return False

    def validate_required_email_user(self) -> None:
        ''' validate if email or username is required '''
        if not self.email and not self.username:
            raise serializers.ValidationError(
                "At least one of 'email' or 'username' is required.")

    def validate_required(self):
        ''' validate if password is required '''
        if not self.password:
            raise serializers.ValidationError(
                'Password is required field'
            )

    def validate_uiniqe(self):
        ''' check unique of email and username '''
        if MyUser.objects.filter(email=self.email).exists():
            raise serializers.ValidationError(
                "You can't use this email. "
                "Choose another, please."
            )
        if MyUser.objects.filter(username=self.username).exists():
            raise serializers.ValidationError(
                "You can't use this username. "
                "Need to come up another"
            )

    def validate_email(self) -> None:
        ''' validate email '''
        if self.email:
            try:
                validate_email(self.email)
            except serializers.ValidationError:
                raise serializers.ValidationError(
                    'value for email is not in correct format'
                )

    def validate_password(self) -> None:
        ''' validate password for ofr length and symbols '''
        no_spaces_password = self.password.replace(
            " ", '').replace("\u2009", "")
        if len(no_spaces_password) < 8:
            raise serializers.ValidationError(
                "Not enough symbols, except space. "
            )
        if not re.search(r'[A-Za-z]', no_spaces_password):
            raise serializers.ValidationError(
                "There is no letters. "
                "Please, add at least one letter."
                "And use Latin. "
            )
        if not re.search(r'\d', no_spaces_password):
            raise serializers.ValidationError(
                "There is no digits. "
                "Please, add at least one digit."
            )
        if not self.count_algo_helper(no_spaces_password):
            raise serializers.ValidationError(
                "Please, figure out "
                "more diversse password."
            )
        print('COME HERE')
        if not (self.validate_substring(no_spaces_password, self.username) and
                self.validate_substring(self.password, self.username[::-1])):
            raise serializers.ValidationError(
                "Please, don't use sequence from "
                "username in password. "
            )

    def validate_all(self) -> None:
        ''' use all validations when create user '''
        self.validate_required_email_user()
        self.validate_required()
        self.validate_email()
        self.validate_password()
        self.validate_uiniqe()
