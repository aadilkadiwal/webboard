from rest_framework import serializers
from django.contrib.auth.models import User
from . models import (
    Board,
    Topic,
    Post
)

class UserSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

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