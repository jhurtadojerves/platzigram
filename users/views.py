"""Users views."""

# Django
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView, FormView
from django.views.generic.edit import FormMixin

# Models
from django.contrib.auth.models import User
from users.models import Profile, Following

# Forms
from users.forms import SignupForm, AddFollowForm


class UserDetailView(LoginRequiredMixin, DetailView):
    """Users detail view."""

    model = User
    object_context_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        if Following.objects.filter(
            to_profile=self.get_object().profile,
            from_profile=self.request.user.profile
        ).exists():
            context['following'] = True
        else:
            context['following'] = False
        return context


class SignupView(FormView):
    """Users sign up view."""

    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view."""

    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']

    def get_object(self):
        """Return user's profile."""
        return self.request.user.profile

    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})


class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = 'users/login.html'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'users/logged_out.html'


class CreateFollowView(LoginRequiredMixin, FormView):
    """Register a new follow"""
    form_class = AddFollowForm
    slug_field = 'username'
    template_name = 'users/follow.html'
    http_method_names = ['post', 'get']

    def post(self, request, *args, **kwargs):
        data = request.POST
        to_profile = get_object_or_404(Profile, pk=data.get('to_profile'))

        follow = Following.objects.filter(
            from_profile=request.user.profile,
            to_profile=to_profile
        )

        if follow.exists():
            follow = Following.objects.get(
                from_profile=request.user.profile,
                to_profile=to_profile
            )
            response = {
                'status': False,
                'message': 'Follow'
            }
            Following.objects.filter(
                from_profile=request.user.profile,
                to_profile=to_profile
            ).delete()
            return JsonResponse(response)
        else:
            follow = Following.objects.create(
                from_profile=request.user.profile,
                to_profile=to_profile
            )
            return JsonResponse({
                'status': True,
                'message': 'Following'
            })
