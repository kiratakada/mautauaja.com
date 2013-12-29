import os
import random

from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.models import User
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


def create_dir_if_not_exists(dir):
    os.umask(0002)
    d = os.path.dirname(dir)

    if not os.path.exists(d):
        os.makedirs(d, 0775)
        #os.chmod(dir, 0775)
        return True

    #os.chmod(dir, 0775)
    return False

def get_questions(data_item=None):
    temp_questions = []
    questions = ItemQuestion.objects.filter(item=data_item).order_by("-date_created")
    if len(questions) > 0:
        for i in questions:
            data = {'question': i.question,
                    'answers': i.get_answers(),
                    'user': i.user,
                    'id': i.id }
            temp_questions.append(data)
    return temp_questions

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            request.session['user_item'] = form.get_user()
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = LoginForm()

    return render_to_response('portal/login.html', {'form': form},
        context_instance=RequestContext(request))

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))

def dashboard(request):
    news = News.objects.all().order_by('-date_created')[:3]
    master_item = MasterItem.objects.all().order_by('-date_created')[:9]

    context = {'news': news, 'msitem': master_item}
    return render_to_response('portal/dashboard.html', context,
        context_instance=RequestContext(request))

def news_details(request, news_id=None):
    news = News.objects.get(id=news_id)
    others_news = News.objects.all().exclude(id=news_id).order_by('date_created')

    context = {'news': news, 'others': others_news}
    return render_to_response('news/news_details.html', context,
        context_instance=RequestContext(request))

def item_details(request, items_id=None):
    data_item = MasterItem.objects.get(id=items_id)
    price_data_list = []

    try:
        request.session['item_item'] = data_item
        others_item = MasterItem.objects.filter(category=data_item.category).exclude(id=items_id).order_by('date_created')

        request.session['others_item'] = others_item
        questions = get_questions(data_item)

        price_data = ItemPrice.objects.filter(item = data_item).order_by("-date_created")
        for i in price_data:
            if i.get_price_rate():
                price_data_list.append(i.get_price_rate())

        context = {'items': data_item, 'others': others_item,
                   'question': questions, 'price_list': price_data_list}

        return render_to_response('items/items_details.html', context,
            context_instance=RequestContext(request))

    except Exception, e:
        print e
        return redirect("dashboard")


def pop_questions(request):
    item = request.session.get('item_item', None)
    user = request.session.get('user_item', None)
    others_item = request.session.get('others_item', None)

    try:
        if request.method == 'POST':
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.cleaned_data['questions']
                ItemQuestion.objects.create(
                    item = item, user = user, question = question)
                return redirect("item_details", items_id=item.id)
        else:
            form = QuestionForm()

        context = {'form': form, 'items_id': item.id, 'label': 'Question',
                   'others': others_item, 'items': item}
        return render_to_response('items/question.html', context,
            context_instance=RequestContext(request))

    except Exception, e:
        print e
        return redirect("dashboard")


def pop_answers(request, question_id):
    item = request.session.get('item_item', None)
    user = request.session.get('user_item', None)
    others_item = request.session.get('others_item', None)

    try:
        try:
            question = ItemQuestion.objects.get(id=question_id)
        except:
            return redirect("dashboard")

        if request.method == 'POST':
            form = QuestionForm(request.POST)
            if form.is_valid():
                answer = form.cleaned_data['questions']

                ItemAnswer.objects.create(
                    question = question,
                    user = user,
                    answer = answer
                )
                return redirect("item_details", items_id=item.id)
        else:
            form = QuestionForm()

        context = {'form': form, 'items_id': item.id, 'label': 'Answer',
                   'others': others_item, 'items': item}
        return render_to_response('items/question.html', context,
            context_instance=RequestContext(request))

    except Exception, e:
        print e
        return redirect("dashboard")

def pop_price(request):
    item = request.session.get('item_item', None)
    user = request.session.get('user_item', None)
    others_item = request.session.get('others_item', None)

    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            comment = form.cleaned_data['comment']
            rate = form.cleaned_data['rate']
            store = form.cleaned_data['store']

            if store:
                price_item = ItemPrice.objects.create(
                    item = item, price = price,
                    store=store)
            else:
                price_item = ItemPrice.objects.create(
                    item = item, price = price)

            rate = PriceRate.objects.create(
                user = user,
                price = price_item,
                rate = rate,
                comment = comment,
            )
            return redirect("item_details", items_id=item.id)
    else:
        form = PriceForm()

    context = {'form': form, 'items': item, 'others': others_item}
    return render_to_response('items/price.html', context,
        context_instance=RequestContext(request))

def pop_store(request):
    item = request.session.get('item_item', None)
    user = request.session.get('user_item', None)
    others_item = request.session.get('others_item', None)

    def handle_uploaded_file(f):
        path = settings.IMAGE_ROOT+'store/'

        create_dir_if_not_exists(path)

        fp = open(os.path.join(path, f.name), 'wb')
        for chunk in f.chunks():
            fp.write(chunk)
        fp.close()

    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store_name = form.cleaned_data['store_name']
            store_address = form.cleaned_data['store_address']
            store_city = form.cleaned_data['store_city']

            try:
                photo = request.FILES['store_photo']
                handle_uploaded_file(photo)
            except:
                pass

            store = MasterStore.objects.create(
                created_by = user,
                store_name = store_name,
                store_address = store_address,
                store_city = store_city,
                store_logo = 'store/'+str(photo),
                store_photo = 'store/'+str(photo),
                )
            messages.success(request, 'Store created : %s' % store_name)
            return redirect('pop_price')

    else:
        form = StoreForm()

    context = {'form': form, 'items': item, 'others': others_item}
    return render_to_response('items/store.html', context,
        context_instance=RequestContext(request))


def store_rate(request, store_id=None):
    item = request.session.get('item_item', None)
    user = request.session.get('user_item', None)
    others_item = request.session.get('others_item', None)

    try:
        try:
            store = MasterStore.objects.get(id=store_id)
        except:
            return redirect("dashboard")

        if request.method == 'POST':
            form = StoreRateForm(request.POST)
            if form.is_valid():
                comment = form.cleaned_data['comment']
                rate = form.cleaned_data['rate']

                StoreRate.objects.create(
                    user = user, store = store,
                    item = item, rate = rate, comment = comment
                )

            return redirect("item_details", items_id=item.id)

        else:
            form = StoreRateForm()

        context = {'form': form, 'others': others_item, 'items': item,
                   'store': store}
        return render_to_response('items/store_rate.html', context,
            context_instance=RequestContext(request))

    except Exception, e:
        print e
        return redirect("dashboard")


def register_user(request):
    def handle_uploaded_file(f):
        path = settings.IMAGE_ROOT+'user/'

        create_dir_if_not_exists(path)

        fp = open(os.path.join(path, f.name), 'wb')
        for chunk in f.chunks():
            fp.write(chunk)
        fp.close()

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            password = form.cleaned_data['password']
            conf_password = form.cleaned_data['conf_password']

            occupation = form.cleaned_data['occupation']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            place_of_birth = form.cleaned_data['place_of_birth']
            date_of_birth = form.cleaned_data['date_of_birth']

            try:
                photo = request.FILES['photo']
                handle_uploaded_file(photo)
            except:
                pass

            try:
                if User.objects.filter(username__iexact= firstname).count() >= 1:
                    #messages.success(request, '%s already exist' % firstname)
                    return redirect('register')

                user = User(username = firstname, first_name = firstname,
                    last_name = lastname, email = email, is_active=True, 
                    is_staff=True)

                user.set_password(password)
                user.save()

                user_profile = UserProfile.objects.create(
                    user=user,
                    occupation = occupation,
                    address = address,
                    phone = phone,
                    place_of_birth = place_of_birth,
                    date_of_birth = date_of_birth,
                    photo = 'user/'+str(photo),
                    is_active = True)

                return redirect('user_login')

            except Exception, e:
                print e
    else:
        form = RegisterForm()

    return render_to_response('portal/register_page.html', {'form':form}, 
        context_instance=RequestContext(request))

def add_news(request):
    user = request.session.get('user_item', None)

    def handle_uploaded_file(f):
        path = settings.IMAGE_ROOT+'news/'
        create_dir_if_not_exists(path)
        fp = open(os.path.join(path, f.name), 'wb')

        for chunk in f.chunks():
            fp.write(chunk)
        fp.close()

    if request.method == 'POST':
        form = AddNewsForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            try:
                photo = request.FILES['photo']
                handle_uploaded_file(photo)
            except:
                pass

            try:
                news = News.objects.create(
                    user = user,
                    title = title,
                    content = content,
                    picture = 'news/'+str(photo)
                )
            except Exception, e:
                print e

            return redirect('dashboard')

    else:
        form = AddNewsForm()

    return render_to_response('portal/news.html', {'form':form, 'title': "Add News"}, 
        context_instance=RequestContext(request))

def edit_news(request, news_id=None):
    user = request.session.get('user_item', None)

    def handle_uploaded_file(f):
        path = settings.IMAGE_ROOT+'news/'
        create_dir_if_not_exists(path)
        fp = open(os.path.join(path, f.name), 'wb')

        for chunk in f.chunks():
            fp.write(chunk)
        fp.close()

    try:
        edit_news = News.objects.get(id=news_id)

        if request.method == 'POST':
            form = AddNewsForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']

                try:
                    photo = request.FILES['photo']
                    handle_uploaded_file(photo)
                except:
                    pass

                edit_news.user = user
                edit_news.title = title
                edit_news.content = content
                edit_news.picture = 'news/'+str(photo)
                edit_news.save()
                return redirect("dashboard")

        else:
            form = AddNewsForm()

        context = {'form':form, 'title': 'Edit News', 'edit_data': edit_news}
        return render_to_response('portal/news.html', context,
            context_instance=RequestContext(request))

    except Exception,e:
        return("dashboard")

def add_item(request):
    user = request.session.get('user_item', None)

    def handle_uploaded_file(f):
        path = settings.IMAGE_ROOT+'items/'
        create_dir_if_not_exists(path)
        fp = open(os.path.join(path, f.name), 'wb')

        for chunk in f.chunks():
            fp.write(chunk)
        fp.close()

    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.cleaned_data['category']
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']

            try:
                photo = request.FILES['photo']
                handle_uploaded_file(photo)
            except:
                pass

            try:
                items = MasterItem.objects.create(
                    category = category,
                    created_by = user,
                    name = name,
                    description = description,
                    picture = 'items/'+str(photo)
                )

            except Exception, e:
                print e

            return redirect('dashboard')

    else:
        form = AddItemForm()

    return render_to_response('portal/items.html', {'form':form, 'title': "Add Items"}, 
        context_instance=RequestContext(request))

def edit_items(request, items_id=None):
    user = request.session.get('user_item', None)

    def handle_uploaded_file(f):
        path = settings.IMAGE_ROOT+'items/'
        create_dir_if_not_exists(path)
        fp = open(os.path.join(path, f.name), 'wb')

        for chunk in f.chunks():
            fp.write(chunk)
        fp.close()

    try:
        edit_item = MasterItem.objects.get(id=items_id)

        if request.method == 'POST':
            form = AddItemForm(request.POST, request.FILES)
            if form.is_valid():
                category = form.cleaned_data['category']
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']

                try:
                    photo = request.FILES['photo']
                    handle_uploaded_file(photo)
                except:
                    pass

                edit_item.user = user
                edit_item.category = category
                edit_item.name = name
                edit_item.description = description
                edit_item.picture = 'items/'+str(photo)
                edit_item.save()
                return redirect("dashboard")

        else:
            form = AddItemForm()

        context = {'form':form, 'title': 'Edit Items', 'edit_data': edit_item}
        return render_to_response('portal/items.html', context,
            context_instance=RequestContext(request))

    except Exception,e:
        return("dashboard")
