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
    occupation = models.CharField(max_length=50,null=True, blank=True)
    address = models.CharField(max_length=50,null=True, blank=True)
    phone = models.CharField(max_length=10,null=True, blank=True)
    place_of_birth = models.CharField(max_length=20,null=True, blank=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    photo = models.CharField(max_length=250,null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField()

    def __unicode__(self):
        return '%s' % (self.user)

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


class MasterStore(models.Model):
    created_by = models.ForeignKey(User)
    store_name = models.CharField(max_length=50)
    store_address = models.CharField(max_length=50)
    store_city = models.CharField(max_length=10)
    store_logo = models.CharField(max_length=50, null=True, blank=True)
    store_photo = models.CharField(max_length=50, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    store_rating = models.IntegerField()

    def __unicode__(self):
        return self.store_name


class MasterItem(models.Model):
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(SubCategory)
    created_by = models.ForeignKey(User)
    store = models.ForeignKey(MasterStore)

    name = models.CharField(max_length=250)
    description = models.TextField()
    picture = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    price = models.IntegerField()
    point = models.IntegerField()

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

    def get_answers(self):
        temp = []

        answer = ItemAnswer.objects.filter(question=self.id).order_by('date_created')
        if len(answer) <= 0:
            return None
        else:
            for i in answer:
                try:
                    photo = UserProfile.objects.get(user=i.user).photo
                except:
                    photo = None

                data = {'answer': i.answer, 'user': i.user, 'photo': photo}
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


class News(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    content = models.TextField()
    picture = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


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

class Order(models.Model):
	ordernumber = models.CharField(max_length=50)
	price = models.IntegerField()
