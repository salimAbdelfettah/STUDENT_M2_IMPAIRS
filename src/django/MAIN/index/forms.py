from django import forms

from .models import ResultModel

class PostForm(forms.ModelForm):

    class Meta:
        model = ResultModel
        fields = ('mots_cles', )