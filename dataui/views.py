import ast, os, random, string

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
            try:
                photo = UserProfile.objects.get(user=i.user).photo
            except:
                photo = None

            data = {'question': i.question,
                    'answers': i.get_answers(),
                    'user': i.user,
                    'date': i.date_created,
                    'id': i.id,
                    'photo': photo}
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
    return HttpResponseRedirect(reverse('dashboard'))

def dashboard(request):
    main_subs = request.GET.get('main_sub', None)
    cat_subs = request.GET.get('child_subs', None)

    category = Category.objects.all()
    category_name, category_sub = '', ''
    news = News.objects.all().order_by('-date_created')[:3]

    if main_subs:
        cat = Category.objects.get(id=main_subs)
        category_name = cat

        master_item = MasterItem.objects.filter(category=cat).order_by('-date_created')[:9]

    elif cat_subs:
        cat = SubCategory.objects.get(id=cat_subs)
        category_sub = cat

        master_item = MasterItem.objects.filter(subcategory=cat).order_by('-date_created')[:9]
    else:
        master_item = MasterItem.objects.all().order_by('-date_created')[:9]

    context = {'news': news, 'msitem': master_item, 'category': category,
               'category_name': category_name, 'category_sub': category_sub}
    return render_to_response('portal/dashboard.html', context,
        context_instance=RequestContext(request))

def news_details(request, news_id=None):
    main_subs = request.GET.get('main_sub', None)
    cat_subs = request.GET.get('child_subs', None)

    try:
        news = News.objects.get(id=news_id)
        others_news = News.objects.all().exclude(id=news_id).order_by('date_created')

        category = Category.objects.all()

        if main_subs or cat_subs:
            return redirect("dashboard")

        context = {'news': news, 'others': others_news, 'category': category}
        return render_to_response('news/news_details.html', context,
            context_instance=RequestContext(request))
    except Exception, e:
        print e
        return redirect("dashboard")

def item_details(request, items_id=None):
    main_subs = request.GET.get('main_sub', None)
    cat_subs = request.GET.get('child_subs', None)
    user = request.session.get('user_item', None)
    category = Category.objects.all()

    try:
        data_item = MasterItem.objects.get(id=items_id)

        request.session['item_item'] = data_item
        others_item = MasterItem.objects.filter(subcategory=data_item.subcategory).exclude(id=items_id).order_by('date_created')

        request.session['others_item'] = others_item
        questions = get_questions(data_item)

        if main_subs or cat_subs:
            return redirect("dashboard")

        try:
            if request.method == 'POST':
                form_questions = QuestionForm(request.POST)
                if form_questions.is_valid():
                    question = form_questions.cleaned_data['questions']

                    ItemQuestion.objects.create(
                        item = data_item, user = user, question = question)
                    return redirect("item_details", items_id=data_item.id)
            else:
                form_questions = QuestionForm()

        except Exception, e:
            return redirect("dashboard")

        context = {'items': data_item, 'others': others_item,
                   'question': questions,
                   'form_questions': form_questions,
                   'form_comment' : CommentSelectForm(), 'category': category}

        return render_to_response('items/items_details.html', context,
            context_instance=RequestContext(request))

    except Exception, e:
        return redirect("dashboard")


#def pop_questions(request):
#    item = request.session.get('item_item', None)
#    user = request.session.get('user_item', None)
#    others_item = request.session.get('others_item', None)
#
#    try:
#        if request.method == 'POST':
#            form = QuestionForm(request.POST)
#            if form.is_valid():
#                question = form.cleaned_data['questions']
#                ItemQuestion.objects.create(
#                    item = item, user = user, question = question)
#                return redirect("item_details", items_id=item.id)
#        else:
#            form = QuestionForm()
#
#        context = {'form': form, 'items_id': item.id, 'label': 'Question',
#                   'others': others_item, 'items': item}
#        return render_to_response('items/question.html', context,
#            context_instance=RequestContext(request))
#
#    except Exception, e:
#        print e
#        return redirect("dashboard")


def pop_answers(request):
    item = request.session.get('item_item', None)
    user = request.session.get('user_item', None)
    others_item = request.session.get('others_item', None)

    if request.method == 'POST':
        data_post =  request.POST.values()
        questions_id = int(data_post[1])
        answer = str(data_post[0])

        if answer != '':
            try:
                question = ItemQuestion.objects.get(id=questions_id)

                x = ItemAnswer.objects.create(
                    question = question,
                    user = user,
                    answer = answer
                )
                return redirect("user_login")

            except Exception, e:
                print e
                return redirect("dashboard")





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

            try:
                photo = request.FILES['photo']
                handle_uploaded_file(photo)
            except:
                pass

            try:
                if User.objects.filter(username__iexact= firstname).count() >= 1:
                    return redirect('register')

                user = User(username = firstname, first_name = firstname,
                    last_name = lastname, email = email, is_active=True, 
                    is_staff=True)

                user.set_password(password)
                user.save()

                data_user = User.objects.get(username=firstname)

                user_profile = UserProfile.objects.create(
                    user=data_user,
                    photo = 'user/'+str(photo),
                    is_active = True,
                    point=0)

                return redirect('user_login')

            except Exception, e:
                pass
    else:
        form = RegisterForm()

    return render_to_response('portal/register_page.html', {'form':form}, 
        context_instance=RequestContext(request))


def add_news(request):
    user = request.session.get('user_item', None)

    try:
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

        return render_to_response('portal/news.html', {'form':form, 'title': "Tambah Berita"},
            context_instance=RequestContext(request))
    except Exception, e:
        return redirect('dashboard')

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

        context = {'form':form, 'title': 'Edit Berita', 'edit_data': edit_news}
        return render_to_response('portal/news.html', context,
            context_instance=RequestContext(request))

    except Exception,e:
        return("dashboard")

def add_item(request):
    user = request.session.get('user_item', None)

    try:
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
                subcategory = form.cleaned_data['sub_category']
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                price = form.cleaned_data['price']
                store = MasterStore.objects.get(id=1)

                try:
                    photo = request.FILES['photo']
                    handle_uploaded_file(photo)
                except:
                    pass

                try:
                    items = MasterItem.objects.create(
                        category = subcategory.category,
                        subcategory = subcategory,
                        created_by = user,
                        name = name,
	                    store = store,
                        description = description,
                        picture = 'items/'+str(photo),
	                    price = int(price),
	                    point = int(price / 100)
                    )

                except Exception, e:
                    print e
                return redirect('dashboard')
        else:
            form = AddItemForm()

        return render_to_response('portal/items.html', {'form':form, 'title': "Tambah Sepatu"},
            context_instance=RequestContext(request))

    except Exception, e:
        print 'Errorrr', e
        return redirect("dashboard")

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
                subcategory = form.cleaned_data['sub_category']
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                price = form.cleaned_data['price']

                try:
                    photo = request.FILES['photo']
                    handle_uploaded_file(photo)
                except:
                    pass

                edit_item.user = user
                edit_item.category = subcategory.category
                edit_item.subcategory = subcategory
                edit_item.name = name
                edit_item.description = description
                edit_item.picture = 'items/'+str(photo)
                edit_item.price = int(price)
                edit_item.point = int(price/100)
                edit_item.save()
                return redirect("dashboard")

        else:
            form = AddItemForm()

        context = {'form':form, 'title': 'Edit Sepatu', 'edit_data': edit_item}
        return render_to_response('portal/items.html', context,
            context_instance=RequestContext(request))

    except Exception,e:
        return("dashboard")

def items_request(request):

    data_item = RequestItem.objects.all()
    try:
        if request.method == 'POST':
            form = ItemRequestForm(request.POST)
            if form.is_valid():
                item_name = form.cleaned_data['item_name']
                description = form.cleaned_data['description']

                rate = RequestItem.objects.create(
                    item_name = item_name,
                    description = description)
                return redirect("items_request")
        else:
            form = ItemRequestForm()

        context = {'form': form, 'data_item': data_item}
        return render_to_response('items/item_request.html', context,
            context_instance=RequestContext(request))

    except Exception, e:
        print e
        return redirect("dashboard")

def about_us(request):
    category = Category.objects.all()
    desc = AboutUs.objects.all().order_by("date_created")

    context = {'description': desc, 'category': category}
    return render_to_response('items/about_us.html', context,
        context_instance=RequestContext(request))

def generate_invoice(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def checkout_temp(request, items_id=None):
	try:
		master_item = MasterItem.objects.get(id=items_id)
		error_message, price, cost = None, 0, 0

		if request.method == 'POST':
			form = CheckoutRequestForm(request.POST)
			if form.is_valid():
				payment = form.cleaned_data['payment']
				cities = form.cleaned_data['cities']
				address = form.cleaned_data['address']

				payment = PaymentGateway.objects.get(id=payment)
				cities = Cities.objects.get(name=cities)
				shiping = Shiping.objects.get(id=1)

				shipping_cost = ShipingCost.objects.get(cities = cities, shiping=shiping)

				if payment.payment_type == 'POINT':
					user_profile = UserProfile.objects.get(user=request.user)
					if user_profile.point >= master_item.point:
						price = master_item.point
						cost = shipping_cost.point
					else:
						error_message = "Point Kamu Tidak Cukup"
				else:
					price = master_item.price
					cost = shipping_cost.price

				if error_message is None:
					order_number = generate_invoice()

					new_order = Order.objects.create(
						order_number = order_number,
						price = price,
						items = master_item,
						shipping_cost = cost,
						total_price = price + cost,
						currency = payment.payment_currency,
						order_status = 'new',
						user = request.user,
						address = address,
						cities = cities,
						payment=payment
					)
					return redirect("confirm_temp", order_id=new_order.id)
		else:
			form = CheckoutRequestForm()

		context = {'item': master_item, 'form': form, 'error_message': error_message}
		return render_to_response('items/checkout_temp.html', context, context_instance=RequestContext(request))

	except Exception as e:
		return redirect("dashboard")

def confirm_temp(request, order_id=None):
	try:
		master_order = Order.objects.get(id=order_id)
		context = {'order': master_order}
		return render_to_response('items/confirm_temp.html', context, context_instance=RequestContext(request))
	except Exception as e:
		return redirect("dashboard")

def accept_order_temp(request, order_id=None):
	try:
		master_order = Order.objects.get(id=order_id)

		if master_order.payment.payment_type == 'POINT':
			user_profile = UserProfile.objects.get(user=master_order.user)
			user_profile.point = user_profile.point - master_order.total_price
			user_profile.save()

			master_order.order_status = 'completed'
			master_order.save()

		else:
			master_order.order_status = 'waiting'
			master_order.save()

		context = {'order': master_order}
		return render_to_response('items/accept_temp.html', context, context_instance=RequestContext(request))

	except Exception as e:
		return redirect("dashboard")

def my_profile(request):
	try:
		master_user = request.user
		master_profile = UserProfile.objects.get(user=request.user)

		my_order = Order.objects.filter(user = master_user, order_status__in=["waiting", "completed"]).order_by("-id").all()
		context = {'user': master_user, 'profile': master_profile, 'order': my_order}
		return render_to_response('items/myprofile.html', context, context_instance=RequestContext(request))

	except Exception as e:
		return redirect("dashboard")

def detail_order_profile(request, order_id=None):
	try:
		order_master = Order.objects.get(id=order_id, user=request.user)
		context = {'order': order_master}
		return render_to_response('items/order_profile.html', context, context_instance=RequestContext(request))
	except Exception as e:
		print e
		return redirect("my_profile")

def admin_report_transaction(request):
	try:
		order_master = Order.objects.filter(order_status__in=["waiting", "completed"]).order_by("-id").all()
		context = {'order': order_master}
		return render_to_response('items/order_admin.html', context, context_instance=RequestContext(request))
	except Exception as e:
		return redirect("dashboard")


def admin_report_transaction_detail(request, order_id=None):
	try:
		order_master = Order.objects.get(id=order_id)
		if request.method == 'POST':
			form = UpdateOrderForm(request.POST)
			if form.is_valid():
				status = form.cleaned_data['status']
				order_master.order_status = status
				order_master.save()
				return redirect("admin_report_transaction")
		else:
			form = UpdateOrderForm()

		context = {'order': order_master, 'form': form}
		return render_to_response('items/order_admin_detail.html', context, context_instance=RequestContext(request))

	except Exception as e:
		return redirect("dashboard")

def export_to_order_csv(request):
	try:
		import csv
		order_master = Order.objects.filter(order_status__in=["waiting", "completed"]).order_by("-id").all()

		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="laporan-transaksi.csv"'

		writer = csv.writer(response, delimiter=';')

		writer.writerow(['Tanggal','OrderId', 'Nama Barang', 'Pembeli', 'Payment', 'Total', 'Currency','Status', 'Alamat Pengiriman'])
		for idata in order_master:
			if idata.order_status == 'waiting':
				status = 'Menunggu Bayar'
			else:
				status = 'Selesai'

			writer.writerow([idata.purchase_date.strftime('%Y-%m-%d %H:%M'), idata.order_number, idata.items.name, idata.user.username,
			    idata.payment.name, idata.total_price, idata.payment.payment_currency, status, idata.address])

		return response

	except Exception as e:
		print e
		return redirect("admin_report_transaction")