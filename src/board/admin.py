from django.contrib import admin
from .models import (
    Board,
    Topic,
    Post
)
'''
Added "Board", "Topic" and "Post" in admin page. So we add, update and delete from there.
'''
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)