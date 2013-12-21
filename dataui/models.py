from django.db import models
from django.contrib.auth.models import User

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

    def __unicode__(self):
        return self.name

class MasterItem(models.Model):
    category = models.ForeignKey(Category)
    created_by = models.ForeignKey(User)

    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    picture = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

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
    store_logo = models.CharField(max_length=50)
    store_photo = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.store_name

class News(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    content = models.TextField()
    picture = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

class ItemPrice(models.Model):
    item = models.ForeignKey(MasterItem, null=True, blank=True)
    store = models.ForeignKey(MasterStore, null=True, blank=True)
    price = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

class StoreRate(models.Model):
    user = models.ForeignKey(User)
    store = models.ForeignKey(MasterStore)
    rate = models.IntegerField()
    comment = models.TextField()
    date_created = models.DateTimeField()

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
