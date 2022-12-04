from django.contrib import admin

# Register your models here.
from .models import Post, Hashtag, Like, Reply

admin.site.register(Post)
admin.site.register(Hashtag)
admin.site.register(Like)
admin.site.register(Reply)
