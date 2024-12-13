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
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded-md border block mt-1 shadow-sm border-gray-300'
            }),
            
            'content': forms.Textarea(attrs={
                'class': 'w-full border shadow-sm p-2 border-gray-300 rounded-md',
                'rows': 4
            }),
            
            'category': forms.Select(attrs={
                'class': 'w-full rounded px-4 py-2'
            }),
            
            'image': ClearableFileInput(attrs={
                'multiple': False
            }),
            
        }
        labels = {
            'is_published': 'Publish'
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'w-full border shadow-sm p-2 border-gray-300 rounded-md',
                    'rows': 4
                }
            )
        }