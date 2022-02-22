from django.urls import path
from . import views as board_views

urlpatterns = [
    path('', board_views.BoardListView.as_view(), name='home-page'),
    path('boards/new/', board_views.new_board, name='new-board'),
    path('boards/<int:pk>/', board_views.board_topics, name='board-topics'),
    path('boards/<int:pk>/new/', board_views.new_topic, name='new-topic'),
    path('boards/<int:pk>/topic/<int:topic_pk>/', board_views.PostListView.as_view(), name='topic-posts'),
    path('boards/<int:pk>/topic/<int:topic_pk>/reply/', board_views.reply_topic, name='reply-topic'),
    path('boards/<int:pk>/topic/<int:topic_pk>/posts/<int:post_pk>/edit/', board_views.PostUpdateView.as_view(), name='edit-post'),
]    