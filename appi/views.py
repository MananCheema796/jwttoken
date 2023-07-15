from django.shortcuts import render
from .serializers import UserSerializer, StudentSerializer, LoginSerializer, ChangePassSerializer, ProfileSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
User = get_user_model()

class UserApi(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'detail':serializer.errors,
            'msg': 'something went Wrong'},
            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        print("Manan")
        user= User.objects.get(email=serializer.data['email'])
        refresh = RefreshToken.for_user(user)
        return Response( {'data':serializer.data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'msg':'User created' }, status=status.HTTP_201_CREATED)


class StudentApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            data = Student.objects.all()
            serializer = StudentSerializer(data, many=True)
            return Response({'data':serializer.data, 'msg':'Data Fetch Successfully'},
            status=status.HTTP_200_OK)
        except:
            return Response({'detail':serializer.errors, 'msg': 'something went Wrong'}, 
            status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
            data = request.data
            serializer= StudentSerializer(data=data)
            if not serializer.is_valid():
                return Response({'detail':serializer.errors, 'msg':'something went Wrong'},
                status=status.HTTP_400_BAD_REQUEST)         
            serializer.save()
            return Response({'data':serializer.data, 'msg':'Data Posted'},
            status=status.HTTP_201_CREATED)   
            

class UserLogin(APIView):
    def post(self, request, format=None):
        serializer =LoginSerializer(data=self.request.data,
        context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({'msg':'User Logged in', 'refresh': str(refresh), 'access': str(refresh.access_token)},
        status=status.HTTP_202_ACCEPTED)


class ProfileViewApi(APIView):
    def get(self, request, format=None):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePassApi(APIView):

    def post(self, request, format=None):
        serializer = ChangePassSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid():
            print("new password", serializer.validated_data["new_password1"])
            return Response({'success': 'Password successfully changed.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)