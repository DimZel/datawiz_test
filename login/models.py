from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    secret = models.CharField(max_length=40)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username
