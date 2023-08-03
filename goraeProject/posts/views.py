from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly ,IsAuthenticated
from .permissions import IsAuthorOrReadOnly, IsReceiverOrReadOnly


#/messages/
class MessageViewSet(ModelViewSet):
    # #authentication 추가 
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    #Permission 기능 : isAuthenticated(읽기권한 x) /IsAuthenticatedOrReadOnly(읽기권한 o )
    permission_classes= [IsAuthorOrReadOnly]

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    # /messages/ 게시글 생성
    def create(self, request, *args, **kwargs):

        #로그인시
        if request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            writer = request.user #request.user를 writer로 받아오기 
            serializer.save(writer=writer)
            serializer.instance.writer.userinfo.points += 10 #작성자 포인트값 
            serializer.instance.writer.userinfo.save()

            #받는사람정보
            receiver = serializer.validated_data.get('receiver')
            if receiver:
                receiver.userinfo.count += 1
                receiver.userinfo.save()
            headers = self.get_success_headers(serializer.data) #성공시 헤더로 전달할 값들을 headers에 담기
            return Response(serializer.data,headers=headers) #response로 data, headers 전송 
        else: #비로그인시
            request.data['writer'] = None
            request.data['receiver'] = None

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,headers=headers) #response로 data, headers 전송 


#개개인 메세지 전달
class ReceivedMessageViewSet(ModelViewSet):
    
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly|IsReceiverOrReadOnly]

    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Message.objects.filter(receiver_id=user_id)
        return queryset
    
    #유저 지정해서 create
    def perform_create(self, serializer) :
        serializer.save(writer=self.request.user) 

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id'] #받는사람
        receiver = get_object_or_404(User, pk=user_id)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        
        serializer.validated_data['writer'] = request.user #작성자 설정
        serializer.validated_data['receiver'] = receiver

        # 편지를 생성
        self.perform_create(serializer)

        #칭찬 보내는 사람 포인트부여
        serializer.instance.writer.userinfo.points += 10
        serializer.instance.writer.userinfo.save()

        #칭찬 받는 사람 카운트 증가 
        receiver = serializer.validated_data.get('receiver') #받은 사람 정보 가져오기
        receiver.userinfo.count += 1
        receiver.userinfo.save()
        
        headers = self.get_success_headers(serializer.data) #성공시 헤더로 전달할 값들을 headers에 담기
        return Response(serializer.data,headers=headers) #response로 data, headers 전송 

    

