"""Posts models"""

# Django
from django.db import models

# Models
from django.contrib.auth.models import User


class Post(models.Model):
    """Post model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    profile = models.ForeignKey(
        'users.Profile',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="posts/photos")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField('users.Profile', through='ReceivedLikes')

    def __str__(self):
        """Return title and username"""
        return "{} by @{}".format(self.title, self.user.username)


class ReceivedLikes(models.Model):
    """Through table for unique_together in relationship"""
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'profile')
