from django.urls import path
from . import views as board_views

urlpatterns = [
    path('', board_views.home, name='home-page'),
    path('boards/<int:pk>/', board_views.board_topics, name='board-topics'),
    path('boards/<int:pk>/new/', board_views.new_topic, name='new-topic'),
    path('boards/<int:pk>/topic/<int:topic_pk>/', board_views.topic_posts, name='topic-posts'),
    path('boards/<int:pk>/topic/<int:topic_pk>/reply/', board_views.reply_topic, name='reply-topic'),
]    