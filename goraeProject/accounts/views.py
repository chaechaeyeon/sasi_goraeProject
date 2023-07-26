from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from posts.models import UserInfo
from .serializers import UserSerializer, UserInfoSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response


#회원가입
class UserCreate(generics.CreateAPIView):
    queryset= User.objects.all()
    serializer_class= UserSerializer

class UserViewSet(viewsets.ModelViewSet) :
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['gets'])
    def get_comment_all(self, request, pk=None) :
        user = self.get_object()
        user_all = user.set_user.all()
        serializer = UserInfoSerializer(user_all, many=True)
        return Response(serializer.data)
    
class UserInfoViewSet(viewsets.ModelViewSet) :
    queryset = UserInfo.objects.all()
    serailizer_class = UserInfoSerializer
    