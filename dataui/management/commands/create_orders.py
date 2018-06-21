from django.core.management.base import BaseCommand
from dataui.models import PaymentGateway, Shiping, Cities, ShipingCost

class Command(BaseCommand):

	def handle(self, *args, **options):
		self.create_payments()
		self.create_shipping()
		self.create_cities()
		self.create_shipping_cost()

	def create_payments(self):
		data = [
			('BRI - ATM Transfer', 52547851235, 'ranli mart', 'ATM', 'IDR'),
			('BCA - ATM Transfer', 7747851238, 'ranli mart', 'ATM', 'IDR'),
			('MartPoint', None, None, 'POINT', 'POINT')
		]

		for idata in data:
			print idata[0], idata[1]
			payments = PaymentGateway.objects.get_or_create(
				name = idata[0],
				payment_number = idata[1],
				payment_name = idata[2],
				payment_type = idata[3],
				payment_currency = idata[4]
			)
			print 'success create payments {}'.format(idata[0])

	def create_shipping(self):
		data = ['POS INDONESIA']
		for idata in data:
			shipping = Shiping.objects.get_or_create(name=idata)
			print 'success create shipping {}'.format(idata)

	def create_cities(self):
		data = ['Cikini', 'Pasar Baru', 'Menteng', 'Palmerah']
		for idata in data:
			cities = Cities.objects.get_or_create(name=idata)
			print 'success create cities {}'.format(idata)

	def save_shipping(self, shipping, citis, price):
		cost = ShipingCost.objects.get_or_create(
			shiping = shipping,
			cities = citis,
			price = price,
			point = price / 1000)
		print 'success create shipping cost {}'.format(citis.name)

	def create_shipping_cost(self):
		shiping = Shiping.objects.all()
		cities = Cities.objects.all()

		for i in shiping:
			for j in cities:
				if j.name == 'Cikini': self.save_shipping(i, j, 25000)
				if j.name == 'Pasar Baru': self.save_shipping(i, j, 15000)
				if j.name == 'Menteng': self.save_shipping(i, j, 10000)
				if j.name == 'Palmerah': self.save_shipping(i, j, 35000)
