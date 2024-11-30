from django.contrib import messages
from .forms import CreatePost
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

# Registeration view
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, 'Password do not match')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
            
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken')
            return redirect('register')
            
        user = User.objects.create_user(username=username, email=email, password=password)
        
        login(request, user)
        messages.success(request, 'Registered successfully')
        return redirect('login')
    return render(request, 'accounts/register.html')


#Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successfull')
            return redirect('home')
        messages.error(request, 'Invalid credentials')
        return redirect('login')
    return render(request, 'accounts/login.html')


# Dashboard view
@login_required
def home_veiw(request):
    return render(request, 'blogs/index.html')


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')


#Create post
def create_posts_view(request):
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            form.save()
            messages.success('Post create successfully')
            return redirect('home')
        else:
            messages.error(request, 'An error occured. Please try again')
    else:
        form = CreatePost()
    return render(request, 'blogs/create_post.html', {'form':form})