from django import forms
from .models import AddBlogModel


class AddBlogContentForm(forms.ModelForm):

    class Meta:
        model = AddBlogModel
        fields = ['title', 'image', 'body']