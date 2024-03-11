from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account import serializers, models
from .renderers import UserRenderer
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

# Create your views here.
class RegisterApiView(APIView):
    serializer_class = serializers.RegisterUserSerializer
    renderer_classes = [UserRenderer]

    def post(self, request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user) 
            return Response({
                'message': 'User registered successfully',
                'user': serializer.data,
                'token': token.key 
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginApiView(APIView):
    serializer_class = serializers.LoginSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            response_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phonenumber': user.phonenumber,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat(),
                'updated_at': user.updated_at.isoformat(),
            }
            return Response({'message': 'Logged In Successfully', 'user': response_data, 'token': serializer.validated_data['token']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserApiView(APIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request) -> Response:
        user_id = request.user.id
        try:
            data = models.User.objects.get(id=user_id)
            serializer = serializers.UserSerializer(data)
            return Response({'message': 'User get successfully', 'user': serializer.data}, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response({'message': 'User Does not exist!'},status=status.HTTP_404_NOT_FOUND)
        
class LogoutApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged Out Successfully'}, status=status.HTTP_200_OK)
