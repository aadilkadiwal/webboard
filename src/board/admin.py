from django.contrib import admin

from .models import Board, Post, Topic

# Added "Board", "Topic" and "Post" Model in admin page.

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
