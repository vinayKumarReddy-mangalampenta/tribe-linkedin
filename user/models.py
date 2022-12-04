from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import uuid


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=300)
    username = models.CharField(
        max_length=200, null=True, blank=True, unique=True)
    about = models.TextField(null=True, blank=True)
    tagline = models.CharField(max_length=2000, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)

    def __str__(self) -> str:
        return self.name
