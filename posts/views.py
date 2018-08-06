"""Posts views."""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.edit import FormMixin
from django.http import JsonResponse
from django.db import IntegrityError

# Models
from posts.models import Post, ReceivedLikes
from users.models import Profile

# Forms
from posts.forms import CreatePostForm, LikePostForm


class PostsFeedView(LoginRequiredMixin, FormMixin, ListView):
    """Return all published posts."""

    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 30
    context_object_name = 'posts'
    form_class = LikePostForm


class PostDetailView(LoginRequiredMixin, DetailView):
    """Return post detail."""

    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'


class CreatePostView(LoginRequiredMixin, CreateView):
    """Create a new post."""

    template_name = 'posts/new.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('posts:feed')


class CreateLikeView(LoginRequiredMixin, FormView):
    """Register a new like y a post"""
    # http_method_names = ['post', ]
    form_class = LikePostForm
    success_url = reverse_lazy('posts:feed')
    template_name = "posts/like.html"

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            post = Post.objects.get(pk=data.get('post'))
            created = ReceivedLikes.objects.create(
                profile=request.user.profile,
                post=post
            )
            return JsonResponse({
                'status': True
            })
        except IntegrityError as e:
            ReceivedLikes.objects.get(
                profile=request.user.profile,
                post=post
            ).delete()
            return JsonResponse({
                'status': False,
                'liked': True
            })
