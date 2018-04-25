from dataui.models import Category, SubCategory
from django.core.management.base import BaseCommand

class Command(BaseCommand):

	def handle(self, *args, **options):
		self.create_category()

	def create_category(self):
		data_category = ['Fashion Wanita', 'Fashion Pria']
		for i in data_category:
			elek = Category.objects.get_or_create(name=i, description=i)
			print 'success create category : {}'.format(i)

		subs_fashion = ['High Heels', 'Sneakers', 'Boots']
		main_fash = Category.objects.get(name='Fashion Wanita')
		for j in subs_fashion:
			subs_j = SubCategory.objects.create(category=main_fash, name=j, description=j)
			print 'success create sub category : {}'.format(j)

		subs_fashion = ['Pantofel', 'Sandal', 'Loafers']
		main_fash = Category.objects.get(name='Fashion Pria')
		for j in subs_fashion:
			subs_j = SubCategory.objects.create(category=main_fash, name=j, description=j)
			print 'success create sub category : {}'.format(j)
