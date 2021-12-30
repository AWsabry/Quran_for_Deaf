from django import forms
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

class CustomUserForm(UserCreationForm):
        
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'country')
        error_messages = {
            'email': {
                'unique': _("This entry has been registered before."),
            },
        }
