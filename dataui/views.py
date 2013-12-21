import os

from datetime import datetime, timedelta
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.views.generic.create_update import delete_object

from dataui.models import *
from dataui.forms import *

from django.conf import settings

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = LoginForm()

    return render_to_response('portal/login.html', {'form': form},
        context_instance=RequestContext(request))

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))

def dashboard(request):
    return render_to_response('portal/dashboard.html', {},
        context_instance=RequestContext(request))


