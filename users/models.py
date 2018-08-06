"""Users models."""

# Django
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Profile model.

    Proxy model that extends the base data with other
    information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    picture = models.ImageField(
        upload_to='users/pictures',
        blank=True,
        null=True
    )

    following = models.ManyToManyField(
        'self',
        through='Following',
        symmetrical=False,
        related_name='follower'
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username."""
        return self.user.username

    def posts_count(self):
        return self.posts.all()

    def post_by_date(self):
        return self.posts.all().order_by('-created')


class Following(models.Model):
    from_profile = models.ForeignKey(
        Profile,
        related_name='from_profile',
        on_delete=models.CASCADE
    )
    to_profile = models.ForeignKey(
        Profile,
        related_name='to_profile',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("from_profile", "to_profile")
