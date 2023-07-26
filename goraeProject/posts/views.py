
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
from .permissions import IsAuthorOrReadOnly

class PostViewSet(ModelViewSet):
    #Permission 기능 : isAuthenticated(읽기권한 x) /IsAuthenticatedOrReadOnly
    permission_classes= [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 포인트부여
        receiver = serializer.validated_data.get('receiver') #받은 사람 정보 가져오기
        receiver.userinfo.points += 1 
        receiver.userinfo.save()

        # 편지생성
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


