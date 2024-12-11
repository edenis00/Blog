from .models import Post, Category
from .forms import CreatePostForm, CommentForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.

# Registeration view
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registered successfully')
            return redirect('login')
        else:
            messages.error(request, 'Registraion Failed. Please try again')
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html')


#Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successfull')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html')


# Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')


# Dashboard view
def home_view(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    categories = Category.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories
    }
    
    return render(request, 'blogs/index.html', context)

#Create post
@login_required
def create_posts_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            messages.success(request,'Post created successfully')
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, 'Post Creation Failed. Please try again')
            return render(request, 'blogs/create_post.html', context)
    else:
        form = CreatePostForm()
        
    context = {'form': form, 'categories': categories}
    return render(request, 'blogs/create_post.html', context)


# Post detail views
@login_required
def post_detial_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_published=True)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post =  post
            comment.author = request.user
            comment.save()
            messages.success(request, "Commented Successfully")
            return redirect('post_detail', post_id=post_id)
        else:
            messages.error(request, "Please fill the field")
            return render(request, 'blogs/post_detail.html', context)
    else:
        form = CommentForm()
        
    comments = post.comments.all()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blogs/post_detail.html', context)

#Edit Post by author
@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    categories = Category.objects.all()
    if request.user != post.author:
        messages.error(request, 'You don\' have permission to edit this post' )
        return redirect('home')
    
    if request.method == 'POST':
        form  = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post updated successfully")
            return redirect('post_detail', post_id)
        else:
            messages.error(request, "Postt updated failed. Please try again")
            return render(request, 'blogs/edit_detail.html', context)
    else:
        form = CreatePostForm(instance=post)
        
    context = {
        'post': post,
        'form': form,
        'categories': categories
    }
    return render(request, 'blogs/edit_detail.html', context)