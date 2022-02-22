import math

from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from markdown import markdown


# Keeping a BOard name unique and description of what the board is all about.
class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    # To make a database readable.
    def __str__(self):
        return self.name

    """
    This function is used to count how many "posts" in each topic.
    The double underscore "topic__board" is used to navigate through the models' relationships.
    Under the hoods, Django built the bridge between the Board-Topic-Post, and built a SQL query to
    retrieve just the posts that belong to a specific board.
    """

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    # This function is used to view which user and what time last post is posted.
    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by("-created_at").first()


"""
In each Board there will be serval topics. The name of user who started the topic and how many time topic has been viewed.
related_name: To create a reverse relationship.
(where "Board" instance will have access a list of "Topic" instance that belong to it)
"""


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name="topics", on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name="topics", on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    # To make a database readable.
    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 6
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    # In reply page limit it to last ten post
    def get_last_ten_posts(self):
        return self.posts.order_by("-created_at")[:10]


# In each topic user can post message and replies those post. Set current date and time while posting mesage.
class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User, null=True, related_name="+", on_delete=models.CASCADE
    )

    # To make a database readable.
    def __str__(self):
        # It's a convenient way to truncate long strings into an arbitrary string size(here we are using 30).
        return self.message[:30]

    # This function is used to use markdown in "post" and "reply".
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode="escape"))
