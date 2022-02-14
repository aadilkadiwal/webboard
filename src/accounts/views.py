from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from board.forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

'''This function is used to register a new user.'''
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

'''
This class base function is used to change the first_name, last_name and email of user.
Login is required to change user info.
'''
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ("first_name", "last_name", "email")
    template_name = 'accounts/my_account.html'
    success_url = reverse_lazy('my-account')

    def get_object(self):
        return self.request.user