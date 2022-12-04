from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .forms import PostCreationForm
from .models import Post, Hashtag, Like, Reply
from user.models import Profile


# temporary
from rest_framework import serializers


def home(request):
    liked_posts = []

    posts = Post.objects.all().order_by('-created', '-last_modified')
    # print(posts[0].likedMembers)

    context = {'posts': posts, 'liked_posts': liked_posts}
    return render(request, 'post/home.html', context)


@login_required(login_url='login')
def create_reply(request, pk):
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        comment = request.POST['comment']
        obj = Reply.objects.create(
            post=post, owner=request.user.profile, content=comment)

    return redirect('/#'+str(obj.id))


@login_required(login_url='login')
def delete_post(request, pk):
    try:
        post = Post.objects.get(id=pk, owner=request.user.profile)
        post.delete()
        messages.success(request, 'post deleted')

        return redirect('home')
    except:
        messages.error(request, 'invalid credentials')

        return redirect('home')


@login_required(login_url='login')
def create_post(request):
    form = PostCreationForm()
    context = {'form': form}

    if request.method == "POST":

        form = PostCreationForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
        else:

            messages.error(request, 'invalid data')

            return render(request, 'post/create-post.html', {'form': form})
        tags = request.POST.get('content').replace(',',  " ").split()

        for word in tags:
            if word.startswith("#"):
                try:
                    tag, created = Hashtag.objects.get_or_create(title=word)
                    tag = Hashtag.objects.get(title=word)
                    data.hashtags.add(tag)
                except ValueError:
                    pass

        data.owner = request.user.profile
        data.save()
        return redirect('home')
    return render(request, 'post/create-post.html', context)


@login_required(login_url='login')
def edit_post(request, pk):
    post = Post.objects.get(id=pk)
    form = PostCreationForm(instance=post)
    context = {'form': form}

    if request.method == "POST":

        form = PostCreationForm(request.POST,  request.FILES, instance=post)
        if form.is_valid():
            data = form.save(commit=False)
        else:

            messages.error(request, 'invalid data')

            return render(request, 'post/create-post.html', {'form': form})
        tags = request.POST.get('content').replace(',',  " ").split()

        for word in tags:
            if word.startswith("#"):
                try:
                    tag, created = Hashtag.objects.get_or_create(title=word)
                    tag = Hashtag.objects.get(title=word)
                    data.hashtags.add(tag)
                except ValueError:
                    pass

        data.owner = request.user.profile
        data.save()
        return redirect('home')
    return render(request, 'post/create-post.html', context)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likePost(request):
    value = request.data['value']
    post = request.data['post']
    post = Post.objects.get(id=post)
    try:
        like = Like.objects.get(post=post, owner=request.user.profile)
        like.value = value
        likesCount = post.getLikesCount
        return Response({'status': 'like updated', 'likesCount': likesCount})
    except:
        vote = Like.objects.create(
            post=post, owner=request.user.profile, value=value)
        likesCount = post.getLikesCount

    return Response({'status': 'like created', 'likesCount': likesCount})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def togglePostLike(request):
    post = request.data['post']
    post = Post.objects.get(id=post)
    print('hello ')
    try:
        like = Like.objects.get(post=post, owner=request.user.profile)
        like.delete()
        likesCount = post.getLikesCount

        return Response({'status': 'like deleted', 'likesCount': likesCount})
    except:
        vote = Like.objects.create(
            post=post, owner=request.user.profile, value='like')
        likesCount = post.getLikesCount

    return Response({'status': 'like created', 'likesCount': likesCount})
