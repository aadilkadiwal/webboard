from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import (
    UserSerialzier,
    BoardSerialzier,
    TopicSerializer,
    PostSerializer
)
from .models import (
    Board,
    Topic,
    Post
) 

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerialzier

class BoardModelViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerialzier

class TopicModelViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer        