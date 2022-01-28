from rest_framework import serializers
from django.contrib.auth.models import User
from . models import (
    Board,
    Topic,
    Post
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class BoardSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['name', 'description']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['subject', 'board', 'starter']     

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['message', 'topic', 'created_by', 'updated_by']          