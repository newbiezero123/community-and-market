# forms.py
from django import forms
from .models import Comment
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': ''  # จะแสดงแทนคำว่า 'Content'
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'เพิ่มความคิดเห็นของคุณที่นี่...'
            })
        }