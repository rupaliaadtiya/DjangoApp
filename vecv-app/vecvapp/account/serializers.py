from rest_framework import serializers
from account import models
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type':'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid Email or Password, Please try again.')
        data['user'] = user
        data['token'] = user.auth_token.key
        return data