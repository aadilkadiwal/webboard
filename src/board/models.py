from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown
import math

class Board(models.Model):
    '''
    unique=True: Keeping a name field unique.
    '''
    name = models.CharField(max_length=30, unique=True)
    '''
    description: Hint of what the board is all about.
    '''
    description = models.CharField(max_length=100)

    '''
    To make a database readable.
    '''
    def __str__(self):
        return self.name

    '''
    This function is used to count how many "posts" in each topic.
    The double underscore "topic__board" is used to navigate through the models' relationships.
    Under the hoods, Django built the bridge between the Board-Topic-Post, and built a SQL query to
    retrieve just the posts that belong to a specific board.
    '''
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()   

    '''
    This function is used to view which user and what time last post is posted.
    '''
    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()     

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    '''
    last_updated: Which is used to define the topics ordering.
    '''
    last_updated = models.DateTimeField(auto_now_add=True)
    '''
    board: Which board is topic belong to.
    related_name: To create a reverse relationship.
    (where "Board" instance will have access a list of "Topic" instance that belong to it)
    '''
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    '''
    starter: Identify the "User" who started the "Topic".
    related_name: To create a reverse relationship.
    (where "User" instance will have access a list of "Topic" instance that belong to it)
    '''
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    '''
    This field is used to store the number of page views.
    '''
    views = models.PositiveIntegerField(default=0)

    '''
    To make a database readable.
    '''
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

    '''In reply page limit it to last ten post'''
    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]

class Post(models.Model):
    '''
    message: Used to store the text of the post replies.
    '''
    message = models.TextField(max_length=4000)
    '''
    related_name: To create a reverse relationship.
    (where "Topic" instance will have access a list of "Post" instance that belong to it)
    '''
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    '''
    created_at: Used to order the "Posts" within a "Topic".
    auto_now_add: Set current date and time when "Post" object is created.
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    '''
    updated_at: To inform the "Users" when and if a given "Post" has been edited.
    '''
    updated_at = models.DateTimeField(null=True)
    '''
    related_name: To create a reverse relationship.
    (where "User" instance will have access a list of "Post" instance that belong to it)
    '''
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    '''
    related_name='+': Don't need of reverse relationship.
    '''
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    '''
    To make a database readable.
    '''
    def __str__(self):
        '''
        It's a convenient way to truncate long strings into an arbitrary string size(here we are using 30).
        '''
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    '''
    This function is used to use markdown in "post" and "reply".
    '''
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))    