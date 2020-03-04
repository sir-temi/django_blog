from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('alias','title', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class':'titleinput form-control'}),
            'text': forms.Textarea(attrs={'class':'form-control', 'id':'text'}),
            # 'author': forms.TextInput(attrs={'class':'authorinput form-control'}),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class':'titleinput form-control', 'Required':'True'}),
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea form-control', 'id':'commentinput', 'Required':'True'}),
        }