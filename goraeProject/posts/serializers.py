from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')

    class Meta:
        model = Post
        fields = ['id', 'content' , 'image', 'writer','receiver']
    
        