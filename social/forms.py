
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Post


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'location']

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Tell people something about yourself...'
        })
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image']

        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "What's on your mind?"
            }),
        }
