from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('boards/<int:pk>/', views.board_topics, name='board-topics'),
    path('boards/<int:pk>/new/', views.new_topic, name='new-topic'),
]    