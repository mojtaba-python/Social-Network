from django import forms
from .models import Post, Comment

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'image')


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'image')

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control'})
        }

class ReplayCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control'})
        }


class SearchForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control'}))