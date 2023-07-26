from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')

    #익명버튼 
    #is_anonymous = serializers.BooleanField(default=False, write_only=True)  # 익명 버튼 필드 추가

    class Meta:
        model = Post
        fields = ['id', 'content' , 'image', 'writer','receiver']
        #exclude =['writer']
        