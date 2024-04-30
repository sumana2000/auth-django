from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

jwt_key = os.getenv('JWT_SECRET')

@api_view(['POST'])
def register_view(request):
    try:
        serializer_obj = UserSerializer(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        serializer_obj.save()
        print(serializer_obj.data)
        return Response(serializer_obj.data)
    except Exception as e:
        return Response(data=str(e),status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    try:
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Wrong password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.timezone.utc)

        }

        token = jwt.encode(payload, jwt_key, algorithm='HS256')

        response = Response(data={'jwt_token':token})

        response.set_cookie(key='jwt_token', value=token, httponly=True) #httponly bcz cookies shouldn't be used by frontend, its only for passing b/w front and backend
        
        return response

    except Exception as e:
        return Response(data=str(e),status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def authuser_view(request):
    try:
        token = request.COOKIES['jwt_token']

        if not token:
            raise AuthenticationFailed('unauthenticated')
        
        payload = jwt.decode(token, jwt_key, algorithms=['HS256'])
        # print(payload)

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            raise AuthenticationFailed('user not found')
        
        print(UserSerializer(user).data)

        return Response(data=UserSerializer(user).data)
    
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def logout_view(request):
    response = Response(data={'logged out'})
    response.delete_cookie('jwt_token')
    return response
    