from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from user.forms import *
from django.views import View
from django.contrib.auth import authenticate, login


class register_user(View):
    def get(self, request):
        if request.user:
            messages.success(request, 'User already Logged in')
            return redirect('home')
        form = CustomUserCreationForm()
        context = {'form': form}
        return render(request, 'user/register.html', context)

    def post(self, request):
        if request.user:
            messages.success(request, 'User already Logged in')
            return redirect('home')
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('login')
        else:
            context = {'form': form}
            return render(request, 'user/register.html', context)


class login_user(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'User already Logged in')
            return redirect('home')
        return render(request, 'user/login.html')

    def post(self, request):
        if request.user.is_authenticated:
            messages.success(request, 'User already Logged in')
            return redirect('home')
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        if user:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

                messages.success(request, 'Login success')

                try:
                    return redirect(request.GET['next'])
                except:
                    return redirect('home')
            else:
                messages.error(request, 'User or password wrong..!')
        else:
            messages.error(request, 'User or password wrong..!')

        return render(request, 'user/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')
