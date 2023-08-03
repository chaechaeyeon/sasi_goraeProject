from rest_framework.routers import SimpleRouter, DefaultRouter
from django.urls import path, include
from .views import MessageViewSet, ReceivedMessageViewSet

#전체 메세지 아이디 확인용
message_router = DefaultRouter(trailing_slash=True)
message_router.register('messages', MessageViewSet, basename='message')

#받은 메세지 
received_router = DefaultRouter(trailing_slash=True)
received_router.register(r'received/(?P<user_id>\d+)', ReceivedMessageViewSet, basename='received')

urlpatterns = [
    path('', include(message_router.urls)),
    path('',include(received_router.urls)),
]