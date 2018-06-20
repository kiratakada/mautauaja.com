from datetime import datetime
from django.contrib.auth.models import User

from dataui.models import Category, SubCategory, UserProfile, MasterItem, MasterStore
from django.core.management.base import BaseCommand

class Command(BaseCommand):

	def handle(self, *args, **options):
		self.create_users()

	def save_to_database(self, data=None, sub_category=None, user_data=None, user_store=None):
		data_item = MasterItem.objects.get_or_create(
			category=sub_category.category,
			subcategory=sub_category,
			created_by=user_data,
			name=data[0],
			description=data[0],
			picture=data[1],
			price=data[2],
			point=int(data[2]/100),
			store=user_store
		)
		print 'success create item {}'.format(data[0])

	def create_users(self):
		user_master = User.objects.get_or_create(
			username = 'ranli',
			first_name = 'Ranli',
			last_name = 'Zega',
			is_staff=True,
			is_active=True,
			is_superuser=True
		)

		user_data = User.objects.get(username='ranli')
		user_data.set_password('ranli')
		user_data.save()

		user_pro = UserProfile.objects.get_or_create(
			user = user_data,
			is_active=True,
			date_of_birth=datetime.now()
		)
		print "success create user {}".format(user_data.username)

		store = MasterStore.objects.get_or_create(
			created_by=user_data,
			store_name = 'Ranli Mart',
			store_address = 'Raden Saleh 2, 188A',
			store_city = 'Jakarta',
			store_logo = 'rl.jpg',
			store_photo = 'rl1.jpg',
			store_rating = 5
		)
		data_store = MasterStore.objects.get(store_name='Ranli Mart')

		# wanita =============================
		sub_category = SubCategory.objects.get(name='High Heels')
		data = [('High Heels - NM210', 'high.jpg', 550000),
		        ('High Heels - NM246', 'high2.jpg', 150000),
		        ('High Heels - NM288', 'high3.jpg', 300000)]
		for idata in data:
			self.save_to_database(data=idata, sub_category=sub_category, user_data=user_data, user_store=data_store)

		sub_category = SubCategory.objects.get(name='Sneakers')
		data = [('Sneakers - NM110', 'sn.jpg', 750000),
		        ('Sneakers - NM156', 'sn2.jpg', 600000),
		        ('Sneakers - NM168', 'sn3.jpg', 800000),]
		for idata in data:
			self.save_to_database(data=idata, sub_category=sub_category, user_data=user_data, user_store=data_store)

		sub_category = SubCategory.objects.get(name='Boots')
		data = [('Boots - NM320', 'bn.jpg', 420000),
		        ('Boots - NM357', 'bn2.jpg', 650000),
		        ('Boots - NM367', 'bn3.jpg', 555000), ]
		for idata in data:
			self.save_to_database(data=idata, sub_category=sub_category, user_data=user_data, user_store=data_store)

		# Pria =============================
		sub_category = SubCategory.objects.get(name='Pantofel')
		data = [('Pantofel - NM410', 'pt.jpg', 560000),
		        ('Pantofel - NM456', 'pt2.jpg', 900000),
		        ('Pantofel - NM488', 'pt3.jpg', 500000),]
		for idata in data:
			self.save_to_database(data=idata, sub_category=sub_category, user_data=user_data, user_store=data_store)

		sub_category = SubCategory.objects.get(name='Loafers')
		data = [('Loafers - NM510', 'lf.jpg', 120000),
		        ('Loafers - NM570', 'lf2.jpg', 350000),
		        ('Loafers - NM599', 'lf3.jpg', 650000), ]
		for idata in data:
			self.save_to_database(data=idata, sub_category=sub_category, user_data=user_data, user_store=data_store)

		sub_category = SubCategory.objects.get(name='Sandal')
		data = [('Sandal - NM610', 'sd.jpg', 80000),
		        ('Sandal - NM660', 'sd2.jpg', 250000),
		        ('Sandal - NM689', 'sd3.jpg', 150000), ]
		for idata in data:
			self.save_to_database(data=idata, sub_category=sub_category, user_data=user_data, user_store=data_store)





