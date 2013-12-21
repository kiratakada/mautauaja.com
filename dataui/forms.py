import os

from datetime import datetime

from cStringIO import StringIO
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.util import ErrorList

from dataui.models import *


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 30, widget=forms.TextInput(), label=u'Username')
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self._user = None

    def get_user(self):
        return self._user

    def clean(self):
        if self.errors:
            return self.cleaned_data

        username = self.cleaned_data.get('username').strip()
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid Username/Password")
        if not user.is_active:
            raise forms.ValidationError("Your account is disabled")

        self._user = user

        return self.cleaned_data

    