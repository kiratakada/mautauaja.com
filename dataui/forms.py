import os
import datetime

from cStringIO import StringIO
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.util import ErrorList

from dataui.models import *

CHOICHES = (
    (1,'Very Bad'),
    (2,'Bad'),
    (3,'Normal'),
    (4,'Very Good'),
    (5,'Excellent'),
)

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

class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=75, widget=forms.TextInput(attrs={'maxlength':'75'}),label=u'Email ')
    firstname = forms.CharField(max_length = 30, widget=forms.TextInput(), label=u'Username')
    lastname = forms.CharField(max_length = 30, widget=forms.TextInput(), label=u'Name')
    password = forms.CharField(max_length = 8, widget=forms.PasswordInput(attrs={'maxlength':'8'}), label=u'Password*') 
    conf_password = forms.CharField(max_length = 8,widget=forms.PasswordInput(attrs={'maxlength':'8'}), label=u'Confirm*')
    occupation = forms.CharField(max_length = 30, widget=forms.TextInput(), label=u'Occupation', required=False)
    address = forms.CharField(max_length = 150, widget=forms.TextInput(), label=u'Address', required=False)
    phone = forms.CharField(max_length = 30, widget=forms.TextInput(), label=u'Phone Number', required=False)
    place_of_birth = forms.CharField(max_length = 30, widget=forms.TextInput(), label=u'Place of birth', required=False)
    date_of_birth = forms.DateField(initial=datetime.date.today, required=False)
    photo = forms.FileField(label="Photo")

    def clean(self):
        if self.errors:
            return

        email = self.cleaned_data['email']
        if email is not None:
            if User.objects.filter(username__iexact= email).count() > 0:
                self.errors['email'] = ErrorList([u'Email account already exist'])

        if self.cleaned_data['password'] != self.cleaned_data['conf_password']:
            self.errors['password'] = ErrorList([u'Password not match'])
            self.errors['conf_password'] = ErrorList([u'Password not match'])

        if len(self.cleaned_data['password']) < 6:
            self.errors['password'] = ErrorList([u'Password at least 6 character'])

        return self.cleaned_data

class QuestionForm(forms.Form):
    questions = forms.CharField(widget=forms.widgets.Textarea())

class AnswersForm(forms.Form):
    answer = forms.CharField(widget=forms.widgets.Textarea())
    
class PriceForm(forms.Form):
    price = forms.IntegerField()
    comment = forms.CharField(widget=forms.widgets.Textarea())
    store = forms.ModelChoiceField(
        MasterStore.objects.all().order_by('date_created'),
        required=False, empty_label='---')

    def clean(self):
        if self.errors:
            return

        return self.cleaned_data

class RatePriceForm(forms.Form):
    comment = forms.CharField(widget=forms.widgets.Textarea())
    rate = forms.ChoiceField(choices=CHOICHES, widget=forms.RadioSelect)

    def clean(self):
        if self.errors:
            return

        return self.cleaned_data


class StoreForm(forms.Form):
    store_name = forms.CharField(max_length = 30, widget=forms.TextInput(), label=u'Store Name')
    store_address = forms.CharField(max_length = 50, widget=forms.TextInput(), label=u'Address')
    store_city = forms.CharField(max_length = 30, widget=forms.TextInput(), label=u'City')
    store_photo = forms.FileField(label="Photo")

    def clean(self):
        if self.errors:
            return

        return self.cleaned_data

class StoreRateForm(forms.Form):
    rate = forms.ChoiceField(choices=CHOICHES, widget=forms.RadioSelect)
    comment = forms.CharField(widget=forms.widgets.Textarea())

    def clean(self):
        if self.errors:
            return
        return self.cleaned_data

class AddNewsForm(forms.Form):
    title = forms.CharField(max_length = 30, widget=forms.TextInput(), label=u'Title')
    content = forms.CharField(widget=forms.widgets.Textarea())
    photo = forms.FileField(label="Photo")

    def clean(self):
        if self.errors:
            return
        return self.cleaned_data

class AddItemForm(forms.Form):
    category = forms.ModelChoiceField(
        Category.objects.all().order_by('name'))

    name = forms.CharField(max_length = 30, widget=forms.TextInput(), label=u'Item Name')
    description = forms.CharField(widget=forms.widgets.Textarea())
    photo = forms.FileField(label="Photo")

    def clean(self):
        if self.errors:
            return
        return self.cleaned_data
    