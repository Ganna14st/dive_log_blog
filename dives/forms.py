from django import forms
from . import models


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = models.BlogPost
        fields = ['title', 'subtitle', 'body', 'pic']


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body']
        labels = {'body': 'New Comment'}


class LogBookForm(forms.ModelForm):
    class Meta:
        model = models.LogBook
        fields = [
            'dive_number',
            'date',
            'time',
            'country',
            'dive_site',
            'guide',
            'buddy',
            'dive_center',
            'duration',
            'depth',
            'nitrox',
            'air_left',
            'notes',
            'pics'
        ]
        labels = {'pics': 'Upload Dive Photos'}
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'dd-mm-yyyy (DOB)', 'class': 'form-control'}),
            'time': forms.TimeInput(format='%H:%M'),
            }
