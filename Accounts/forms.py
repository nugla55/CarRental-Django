from django import forms

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.widgets import FileInput
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from Reservations.models import Visitor


class SignupForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("username exists")
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")

        return self.cleaned_data


class VisitorForm(ModelForm):
    class Meta:
        model = Visitor
        fields = '__all__'
        exclude = ['user', 'role', 'email', 'username']

        labels = {
            'username': _('Usename:'),
            'first_name': _('Name:'),
            'last_name': _('Surname:'),
            'profile_pic': _('Profile image:'),
        }

        widgets = {
            'profile_pic': FileInput(),
        }


class LoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email')
