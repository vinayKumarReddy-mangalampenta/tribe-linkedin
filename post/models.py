from django.db import models
import uuid
from user.models import Profile
from django.db.models import Count
from .get_curr_user import current_request


class Hashtag(models.Model):
    title = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    image = models.ImageField(null=True, blank=True)
    likesCount = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          editable=False, primary_key=True)

    def __str__(self) -> str:
        return str(self.title)

    @property
    def likedMembers(self):
        request = current_request()
        data = self.like_set.get(owner=request.user.profile)
        print(data.value)
        return data

    @property
    def getLikesCount(self):
        count = self.like_set.all().count()
        self.likesCount = count
        self.save()

        return self.likesCount


class Like(models.Model):
    VOTE_TYPE = (
        ('like', "like"),
        ('love', 'love'),
        ('cheers', 'cheers'),
        ('claps', 'claps'),
        ('hundred', 'hundred'),
        ('laugh', 'laugh')
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          editable=False, primary_key=True)

    def __str__(self) -> str:
        return str(self.post)

    class Meta:
        unique_together = [['owner', 'post']]


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    likesCount = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          editable=False, primary_key=True)

    def __str__(self) -> str:
        return str(self.content)
