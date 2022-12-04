from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('create-post/', create_post, name='create-post'),
    path('api/like-post/', likePost, name='like-post'),
    path('api/toggle-like-post/', togglePostLike, name='toggle-like'),
    path('report-comment/<str:pk>/', create_post, name='report-comment'),


    path('reply-post/<str:pk>/', create_reply, name='reply-post'),
    path('delete-post/<str:pk>', delete_post, name='delete-post'),
    path('edit-post/<str:pk>', edit_post, name='edit-post')
]
