from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Topic

"""
ModelForm is associated with the "Topic" model.
The "subject" in the fields list inside the Meta class is referring to the "subject" field in the "Topic" model.
Defining an extra field named "message" in a form. This refer to the message in the "Post" we want to save.
"""


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 5, "placeholder": "What is on your mind?"}
        ),
        max_length=4000,
        help_text="The max length of the text is 4000",
    )

    class Meta:
        model = Topic
        fields = ["subject", "message"]


"""
UserCreationForm: Django built-in form.
Fields in UserCreationForm by default: username, password, password confirmation.
Created a new field as a email in form.
"""


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["message"]
