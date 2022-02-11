from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from .models import (
    Board,
    Topic,
    Post
)    
from .forms import (
    NewTopicForm,
    PostForm
)

'''
This function is used to view as a home page.
It show all "Board" data.
How many "Post" and "Topic" are there in "Board" topic.
It also show when last "Post" is post.
'''
def home(request):
    boards = Board.objects.all()
    return render(request, 'board/home.html', {'boards': boards})

'''
This function is used to view of all "Topic" of each "Board".
It show starter (name of user who created the topic).
How many Replies and Views are there of each topic.
It also show when the topic is last updated.
'''
def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    '''
    "annotate" queryset method to generate a new "column" on the fly.
    This new column, which will be translated into a property, accessible via
    "topic.replies" contain the count of posts a given topic has.
    '''
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1) 
    return render(request, 'board/topics.html', {'board': board, 'topics': topics})    

'''
This function is used to create a new topic.
Login is required before creating a new topic.
Dealing with one argument as "pk" which is used to identify the "Board".
'''
@login_required
def new_topic(request, pk):
    '''It verify whether the "Board" is exist or not.'''
    board = get_object_or_404(Board, pk=pk)
    '''
    To check whether request is "POST" or "GET".
    If request is "POST" means that user is trying to submit some data.
    '''
    if request.method == 'POST':
        '''We instantiate a form instance passing the "POST" data to the form'''
        form = NewTopicForm(request.POST)
        '''To check whether Form data is valid or not'''
        if form.is_valid():
            '''
            The "board" and "starter" field are non-nullable at the database level.
            Which means if we save the form without providing a "board" and "starter" value,
            it will throw an exception.
            So what we do is, save the form changing the commit flag to False so it will prepare
            all the model fields, then we provide the extra data which is mandatory(board and starter)
            and manually save the topic calling topic.save()
            '''
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            '''
            Redirecting to the created Topic page.
            Using "topic.pk" because "topic" is an object(Topic model instance) and
            ".pk" accessing the "pk" property of the Topic model instance. 
            '''
            return redirect('topic-posts', pk=pk, topic_pk=topic.pk)

    else:
        '''If request is "GET" initializing a new empty form.'''
        form = NewTopicForm()    

    return render(request, 'board/new_topic.html', {'board': board, 'form': form})

''''
This function is used to create a post.
Login is required before posting any post.
Dealing with one argument "pk" which is used to identify "Board",
Dealing with second argument "topic_pk" which is used to identify which topic to retrieve from the database.
'''
@login_required
def topic_posts(request, pk, topic_pk):
    '''
    "board__pk": Is used to access the data of "Board"
    "topic_pk": Is used to view data
    '''
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    '''Keep track of the number of views a given topic is receiving.'''
    topic.views += 1
    topic.save()
    return render(request, 'board/topic_posts.html', {'topic': topic})

'''
This function is used to reply message on specific post.
Dealing with one argument "pk" which is used to identify "Board",
Dealing with second argument "topic_pk" which is used to identify which topic to retrieve from the database.
'''
@login_required
def reply_topic(request, pk, topic_pk):
    '''
    "board__pk": Is used to access the data of "Board"
    "topic_pk": Is used to view data
    '''
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            '''After posting a reply, the user is redirect back to the topics posts'''
            return redirect('topic-posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'board/reply_topic.html', {'topic': topic, 'form': form})