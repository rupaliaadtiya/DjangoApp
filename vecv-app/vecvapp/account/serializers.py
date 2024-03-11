from rest_framework import serializers
from account import models
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'first_name', 'last_name' ,'phonenumber', 'password')
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}

    def create(self, validated_data):
        user = models.User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phonenumber=validated_data['phonenumber'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type':'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid Email or Password, Please try again.')
        
        if not hasattr(user, 'auth_token'):
            token = Token.objects.create(user=user)
        else:
            token = user.auth_token

        data['user'] = user
        data['token'] = user.auth_token.key
        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'