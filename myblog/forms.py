from django import forms
from .models import Post, Comment

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
            'is_published'
        ]
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']    