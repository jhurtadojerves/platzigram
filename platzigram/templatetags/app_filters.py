"""Custom templatetags"""

# Django
from django import template

# Models
from posts.models import Post, ReceivedLikes

register = template.Library()


def liked(post, profile):
    liked = 'black'
    if ReceivedLikes.objects.filter(
        post__id=post,
        profile__id=profile
    ).exists():
        liked = 'red'
    return liked

register.filter('liked', liked)
