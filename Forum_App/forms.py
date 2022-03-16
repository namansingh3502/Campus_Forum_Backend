from django.forms import ModelForm
from .models import Post, Post_Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'media_count']


class CommentForm(ModelForm):
    class Meta:
        model = Post_Comment
        fields = ['body', 'post']
