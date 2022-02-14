from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)     
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from django.views.generic import (
    ListView,
    UpdateView
)
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
This class based view function is used to view as a home page.
It show all "Board" data.
How many "Post" and "Topic" are there in "Board" topic.
It also show when last "Post" is post.
'''
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'board/home.html'

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
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)
    '''Function Base View Pagination: Paginate queryset in pages of 6 each.'''
    paginator = Paginator(queryset, 6)

    try:
        '''See the current page out of total page.'''
        topics = paginator.page(page)
    except PageNotAnInteger:
        '''Fallback to the first page.'''
        topics = paginator.page(paginator.num_pages)
    except EmptyPage:
        '''
        Probably the user tried to add a page number.
        in the url, so fallback to the last page.   
        '''
        topics = paginator.page(paginator.num_pages)    
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
This class base function is used to create a post.
Login is required before posting any post.
'''
@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'board/topic_posts.html'
    paginated_by = 1

    def get_context_data(self, **kwargs):
        '''Control the view counting system '''
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            '''Keep track of the number of views a given topic is receiving.'''
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
            
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        "board__pk": Is used to access the data of "Board".
        "topic_pk": Is used to view data.
        '''
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset
   
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

            '''Updating the last update.'''
            topic.last_updated = timezone.now()
            topic.save()

            '''
            Sending the user to the last page.
            In the topic_post_url building a URL with the last page and adding an anchor to the element with id equals to the post ID.
            '''
            topic_url = reverse('topic-posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )
            '''After posting a reply, the user is redirect back to the topics posts'''
            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'board/reply_topic.html', {'topic': topic, 'form': form})

'''
This generic class based view is used to edit post.
Can't decorate with the "@login_required" decorator.
In class-based views it's common to decorate the "dispatch" method. All requests pass through this method, so it's safe to decorate it.
'''
@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'board/edit_post.html'
    '''To identify the name of the keyword argument used to retrieve the Post object.'''
    pk_url_kwarg = 'post_pk'
    '''
    To rename it to post instead.
    Navigating through the post object: "post.topic.board.pk".
    If I didn't set the context_object_name to post. It would be "object.topic.board.pk".
    '''
    context_object_name = 'post'

    '''Override get_queryset to '''
    def get_queryset(self):
        '''
        Reusing the "get_queryset" method from the parent class.
        Adding an extra filter to the queryset, filtering the post using the logged in user, available inside the project.
        '''
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    '''Override the form_valid method, to set some extra field such as the updated_by and updated_at.'''
    def form_valid(self, form):
        post = form.save(commit=False) 
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic-posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)  