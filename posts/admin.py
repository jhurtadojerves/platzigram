"""Post admin classes."""

# Django
from django.contrib import admin

# Models
from posts.models import Post, ReceivedLikes

admin.site.register(Post)
admin.site.register(ReceivedLikes)
