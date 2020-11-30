from django.contrib.auth.models import User
from .models import Profile, Post
from django.contrib.auth.forms import UserCreationForm
from django import forms


class PostCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'created-post-title',
            'placeholder': 'New post title here...',
            'autocomplete': 'off',
        })

        self.fields['header'].widget.attrs.update({
            'class': 'created-post-header',
            'style': 'display: none',
            'id': 'file',

        })
        self.fields['snippet'].widget.attrs.update({
            'class': 'created-post-snippet',
            'placeholder': 'Post Snippet here...',
            'autocomplete': 'off',
        })

        self.fields['body'].widget.attrs.update({
            'class': 'created-post-body',
        })

        self.fields['tags'].widget.attrs.update({
            'class': 'created-post-tags',
        })

    class Meta:
        model = Post
        fields = ['header', 'title', 'tags', 'snippet', 'body']


class UserRegisterPage(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilePageForm(forms.ModelForm):
    profile = forms.ImageField(
        label='', widget=forms.FileInput, required=False)

    class Meta:
        model = Profile
        fields = ['profile']
