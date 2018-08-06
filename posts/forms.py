"""Posts forms."""

# Django
from django import forms

# Models
from posts.models import Post, ReceivedLikes


class CreatePostForm(forms.ModelForm):
    """Post model form"""
    class Meta:
        """Form settings."""
        model = Post
        fields = ('user', 'profile', 'title', 'photo')


class LikePostForm(forms.ModelForm):
    """Form to add like"""
    class Meta:
        model = ReceivedLikes
        fields = ('profile', 'post')
