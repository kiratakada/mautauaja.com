import math

from django.db import models
from django.contrib.auth.models import User

from itertools import groupby

from django.db import connection

class Roles(object):
    ADMIN = 0x01
    CLIENT = 0x02

    CHOICES = {
        ADMIN: 'Admin',
        CLIENT: 'Client'}

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    occupation = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    place_of_birth = models.CharField(max_length=20)
    date_of_birth = models.DateTimeField()
    photo = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.user.first_name

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def get_sub_category(self):
        subs_category = []
        subs = SubCategory.objects.filter(category=self.id)

        return subs

    def __unicode__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class MasterItem(models.Model):
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(SubCategory)
    created_by = models.ForeignKey(User)

    name = models.CharField(max_length=20)
    description = models.TextField()
    picture = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_minimum_price(self):
        temp = []
        price_stat = 0
        data_price = ItemPrice.objects.filter(item=self.id)

        if data_price:
            for item in data_price:
                temp.append(int(item.price))

            temp.sort()
            price_stat = temp[0]

        return price_stat

    def get_store_list(self):
        store_list = []
        cursor = connection.cursor()

        sql = """
            select
                store_id as id,
                store_id as store
            from
                dataui_itemprice
            where
                item_id = %s
                group by store_id;
        """ % (self.id)
        cursor.execute(sql)
        total = cursor.fetchall()

        for i in total:
            if i[0]:
                store = MasterStore.objects.get(id=i[0])
                store_list.append(store)

        return store_list

class ItemReview(models.Model):
    item = models.ForeignKey(MasterItem)
    user = models.ForeignKey(User)
    review = models.TextField()

    def __unicode__(self):
        return self.review


class ItemQuestion(models.Model):
    item = models.ForeignKey(MasterItem)
    user = models.ForeignKey(User)
    question = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def get_answers(self):
        temp = []

        answer = ItemAnswer.objects.filter(question=self.id).order_by('date_created')
        if len(answer) <= 0:
            return None
        else:
            for i in answer:
                data = {'answer': i.answer, 'user': i.user}
                temp.append(data)
            return temp

    def __unicode__(self):
        return self.question


class ItemAnswer(models.Model):
    question = models.ForeignKey(ItemQuestion)
    user = models.ForeignKey(User)
    answer = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.answer

class MasterStore(models.Model):
    created_by = models.ForeignKey(User)

    store_name = models.CharField(max_length=50)
    store_address = models.CharField(max_length=50)
    store_city = models.CharField(max_length=10)
    store_logo = models.CharField(max_length=50, null=True, blank=True)
    store_photo = models.CharField(max_length=50, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.store_name

    def get_store_rate(self):
        data = []
        cursor = connection.cursor()

        sql = """
            select
                store_id as store_id,
                sum(rate)/count(*) as rate,
                sum(rate) as total_rate,
                count(*) as record
            from
                dataui_storerate
            where
                store_id = %s
            group by store_id
        """ % (self.id)
        cursor.execute(sql)
        total = cursor.fetchall()

        for i in total:
            data = {'rate': i[1],
                    'total': i[3],
                    }
        return data

        #data, temp = None, []
        #
        #rate = StoreRate.objects.filter(store=self.id).order_by("date_created")
        #for i in rate:
        #    temp.append(
        #        {'user': i.user.username, 'rate': int(i.rate),
        #        'comment': i.comment})
        #return temp


class News(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    content = models.TextField()
    picture = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

class ItemPrice(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(MasterItem, null=True, blank=True)
    store = models.ForeignKey(MasterStore, null=True, blank=True)
    price = models.FloatField()
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.price

    def get_price_rate(self):
        data = []
        cursor = connection.cursor()

        sql = """
            select
                price_id,
                count(*) as total,
                sum(rate)/count(*) as rate,
                sum(rate) as total_rate
            from
                dataui_pricerate
            where
                price_id = %s
            group by price_id
        """ % (self.id)
        cursor.execute(sql)
        total = cursor.fetchall()

        for i in total:
            data = {'rate': i[2],
                    'total': i[1],
                    }
        return data


class StoreRate(models.Model):
    user = models.ForeignKey(User)
    store = models.ForeignKey(MasterStore)
    rate = models.IntegerField()
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s-%s' % (self.user, self.rate)

class PriceRate(models.Model):
    user = models.ForeignKey(User)
    price = models.ForeignKey(ItemPrice)
    rate = models.IntegerField()
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s-%s' % (self.user, self.rate)

class RequestItem(models.Model):
    item_name = models.CharField(max_length=50)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s-%s' % (self.item_name, self.description)

class AboutUs(models.Model):
    desc = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.desc
