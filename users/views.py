from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import UserSerializer

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
        pass
    except Exception as e:
        return Response(data=str(e),status=status.HTTP_400_BAD_REQUEST)

