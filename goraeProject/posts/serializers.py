from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Message

class MessageSerializer(ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.userinfo.nickname')
    class Meta:
        model = Message
        fields = ['id', 'content' , 'image', 'writer', 'receiver']

