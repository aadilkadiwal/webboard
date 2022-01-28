from rest_framework.routers import DefaultRouter
from board import api

router = DefaultRouter()
router.register('boards', api.BoardModelViewSet, basename='boards')
router.register('topics', api.TopicModelViewSet, basename='topics')
router.register('posts', api.PostModelViewSet, basename='posts')