from django import forms
from mainapp import models as mainapp_models


class CommentForm(forms.ModelForm):

    class Meta:
        model = mainapp_models.Comment
        fields = ('text',)


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)


class BasketForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
