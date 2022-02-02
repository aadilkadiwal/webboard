from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import (
    Board,
    Topic,
    Post
)    
from .forms import NewTopicForm

def home(request):
    boards = Board.objects.all()
    return render(request, 'board/home.html', {'boards': boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk) 
    return render(request, 'board/topics.html', {'board': board})    

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()     # TODO: get the currently login user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            board = topic.board
            user = topic.starter
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board-topics', pk=board.pk)  # TODO: redirect to the created topic page

    else:
        form = NewTopicForm()    

    return render(request, 'board/new_topic.html', {'board': board, 'form': form})