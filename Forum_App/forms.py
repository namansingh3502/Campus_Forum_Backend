from django.forms import ModelForm
from .models import Post, PostComments


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']


class CommentForm(ModelForm):
    class Meta:
        model = PostComments
        fields = ['body', 'post']
