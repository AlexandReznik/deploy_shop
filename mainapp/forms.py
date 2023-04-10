from django import forms
from mainapp import models as mainapp_models


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)


class BasketForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)


class ProductFeedbackForm(forms.ModelForm):

    def __init__(self, *args, product=None, user=None, **kwargs):
        ret = super().__init__(*args, **kwargs)
        if product and user:
            self.fields["product"].initial = product.pk
            self.fields["user"].initial = user.pk
        return ret

    class Meta:
        model = mainapp_models.ProductFeedback
        fields = ("product", "user", "feedback", "rating")
        widgets = {
            "product": forms.HiddenInput(),
            "user": forms.HiddenInput(),
            "rating": forms.RadioSelect(),
        }
