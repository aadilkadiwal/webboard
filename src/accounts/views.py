from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from board.forms import SignUpForm

def signup(request):
    '''To check whether request is "POST" or "GET".'''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        '''To check whether the given user data is valid or not.'''
        if form.is_valid():
            '''To save all information of form in user'''
            user = form.save()
            login(request, user)
            '''Sucessfully creating accout direct to home-page'''
            return redirect('home-page')
    else:
        '''If request is "GET" it will return an empty form.'''        
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})