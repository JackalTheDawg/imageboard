from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .utility.managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """custom auth model"""

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    email = models.CharField(_("email address"), unique=True, max_length=100, blank=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(blank=False, max_length=30)
    surname = models.CharField(blank=False, max_length=30)

    birthday = models.DateField()
    gender = models.CharField(max_length=20)

    profile_picture = models.CharField(max_length=1000, default='static/media/assets/default_pp.png')


class Post(models.Model):

    sender = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)

    location = models.CharField(max_length=10000, blank=False)
    date = models.DateField(default=timezone.now)
    text = models.CharField(max_length=1000)

    content = models.CharField(max_length=1000, blank=True, null=True)
    mime = models.CharField(max_length=20, blank=True, null=True)

    liked_by = models.ManyToManyField(Profile, related_name='liked', blank=True)
    posted_as = models.CharField(max_length=9, default='profile')


class Community(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=300, blank=True)
    private = models.BooleanField(default=False)

    image = models.CharField(max_length=1000, default='static/media/assets/default_pp.png')

    admins = models.ManyToManyField(Profile, related_name='community_admins')

    followers = models.ManyToManyField(Profile, related_name='community_followers')


class FollowsProfiles(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1', null=True)
    page = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=True, related_name='profile2')


class Commentary(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    text = models.CharField(max_length=1000)
    content = models.CharField(max_length=1000, blank=True, null=True)

    date = models.DateField(default=timezone.now)
    liked_by = models.ManyToManyField(Profile, related_name='likes')
