from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Category, Comment
from django.contrib.auth import login, logout
from .forms import CreatePostForm, CommentForm
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
            messages.success(request, 'Registered successfully!')
            return redirect('home')
        else:
            # messages.error(request, 'Registraion failed. Please try again')
            messages.error(request, form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form':form})


#Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successfull!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


# Dashboard view
def home_view(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    categories = Category.objects.all()
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'posts': page_obj
    }
    
    return render(request, 'blogs/index.html', context)


#Create post
@login_required
def create_posts_view(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            messages.success(request,'Post created successfully!')
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, 'Failed to create post. Please try again')
            return render(request, 'blogs/create_post.html', context)
    else:
        form = CreatePostForm()
    
    categories = Category.objects.all()
    context = {'form': form, 'categories': categories}
    return render(request, 'blogs/create_post.html', context)


# Post detail views
@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post.objects.prefetch_related('comments'), id=post_id, is_published=True)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post =  post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('post_detail', post_id=post_id)
        else:
            messages.error(request, "Comment cannot be empty")
    else:
        form = CommentForm()
        
    
    context = {
        'post': post,
        'comments': post.comments.all().order_by('-created_at'),
        'form': form,
    }
    return render(request, 'blogs/post_detail.html', context)


#Edit Post by author
@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user != post.author:
        messages.error(request, 'You don\'t have permission to edit this post.' )
        return redirect('post_detail', post.id)
    
    if request.method == 'POST':
        form  = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('post_detail', post_id)
        else:
            messages.error(request, "Failed to update post. Please try again")
    else:
        form = CreatePostForm(instance=post)
    
    categories = Category.objects.all()
    context = {
        'post': post,
        'form': form,
        'categories': categories
    }
    return render(request, 'blogs/edit_detail.html', context)


#Edit Comment 
@login_required
def edit_comment_view(request,  id):
    comment = get_object_or_404(Comment, id=id)
    
    if request.user != comment.author:
        messages.error(request, "You don't have permission to edit this comment")
        return redirect('post_detail', comment.post.id)
        
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            messages.success(request, "Comment updated successfully!")
            return redirect('post_detail', comment.post.id)
        else:
            messages.error(request, "Failed to update comment. Please try again")
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blogs/edit_comment.html', {'form': form})