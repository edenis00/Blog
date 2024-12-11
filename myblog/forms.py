from django import forms
from .models import Post, Comment
from django.forms import ClearableFileInput

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
            'image',
            'is_published'
        ]
        widget = {
            'image': ClearableFileInput(attrs={'multiple': False})
        }
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widget = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comments here'}),
        }