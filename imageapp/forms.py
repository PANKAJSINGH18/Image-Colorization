from django import forms

class Imageforms(forms.Form):
    image = forms.ImageField()
    