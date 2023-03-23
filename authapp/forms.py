from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
        )
    field_classes = {"username": UsernameField}

    def clean_age(self):
        data = self.cleaned_data.get("age")
        if data < 10 or data > 100:
            raise ValidationError(_("Please, enter a valid age!"))
        return data
