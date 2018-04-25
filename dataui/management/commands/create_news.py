from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from dataui.models import News


class Command(BaseCommand):

	def handle(self, *args, **options):
		self.create_news()

	def create_news(self):
		user_data = User.objects.get(username='ranli')

		news1 = News.objects.create(
			user = user_data,
			title = 'Retro Khas 80-an, Sneaker Ini Buat Anda Tampil Modern dan Estetik',
			picture = 'news1.jpg',
			content = """
				Ketika memilih sneaker, apa yang menjadi pertimbangan Anda? Salah satunya tentu adalah gaya dan penampilan Anda sendiri, bukan?

				Puma, sebagai label olahraga global mendesain ulang salah satu sneaker andalannya yang terinspirasi dengan sentuhan retro, yaitu Puma RS. Melucuti seluruh siluet RS, Puma menambahkan detail modern dan estetik, serta bahan yang bisa mendukung performa teknis.

				Sneaker Puma RS kali ini memiliki "O" pada lisensi untuk memperkuat pernyataan bahwa sneaker ini didesain guna merayakan setiap momen unik dari setiap kultur, disebut sebagai future meets retro. Sneaker Puma RS sendiri terkenal dengan inovasi dan bantalan sepatu premium khas tahun 80-an.

				Pada waktu itu, sneaker Puma RS ini adalah jawaban atas permintaan pasar akan sepatu lari yang stabil. Sneaker RS O sendiri adalah cara Puma bernostalgia pada estetika masa lalu dan berekspektasi terhadap masa depan.
			"""
		)
		print 'create news 1 OK'

		news2 = News.objects.create(
			user=user_data,
			title='Mulai Jalani Gaya Hidup Sehat dari Pilihan Sepatu Athleisure',
			picture='news2.jpg',
			content="""
					Sepatu tidak hanya dapat menunjang penampilan dan kecantikan, namun menjadi sahabat untuk menjalani gaya hidup. Keds sebagai salah brand sepatu ternama meluncurkan koleksi terbarunya, Keds Studio.

					Keds Studio ini merupakan sebuah rangkaian koleksi sepatu yang hadir sebagai evolusi dari siluet klasik Keds. Koleksi ini pun memiliki tiga fitur utama, yakni breathable, lightweight, dan stretchable
					
					Memiliki desain yang modern, Keds Studio mempunyai warna netral yang cantik dan cerah. Desainnya memiliki gaya yang lebih athleisure daripada koleksi sepatu Keds sebelumnya. koleksi Keds Studio ini didesain memberikan kenyamanan bagi perempuan aktif.

					"Dilengkapi dengan teknologi dan bahan Dri-Freeze lining yang dapat membantu menjaga tingkat kelembapan kaki dan menjaganya agar tetap dingin. Keds Studio cocok untuk perempuan modern yang aktif dan ingin menjalani gaya hidup sehat," ujar Reni Lauw Brand Manager Keds Indonesia.

					Koleksi Keds Studio akan hadir di Indonesia dengan dua varian, Studio Leap dan Studio Live. Masing-masing varian hadir dalam dua warna, yakni hitam dan abu-abu. Koleksi Keds Studio ini dibanderol dengan harga Rp 999 ribu.
					
					"""
			)
		print 'create news 2 OK'

		news3 = News.objects.create(
			user=user_data,
			title='Adidas Luncurkan Siluet Sol Sepatu Lari dengan Teknologi Tinggi',
			picture='news3.jpg',
			content="""
					Sebagai sebuah sport brand ternama, adidas selalu menghadirkan beragam inovasi-inovasi mengagumkan. Salah satunya adalah sepatu adidas running dengan siluet high-performance running pertama berteknologi BOOST.
					
					Lima tahun setelah merilisnya, kini teknologi ini diperbaharui dan dirilis kembali dalam warna hitam dan kuning yang khas sebagai adidas anniversary pack, Energy BOOST OG dan Energy BOOST. Seperti rilis yang diterima oleh Liputan6.com, Selasa (6/2/2018) BOOST adalah teknologi lightweight cushioning superior yang mengembalikan energi di setiap langkah.
					
					Material state-of-the-art yang mendefinisikan kategori adidas Running dan telah memecahkan dua rekor maraton dunia dengan atlet unggulan Mary Keitany dan Dennis Kimetto, kini merayakan lima tahun berada di garis inovasi terdepan.
					
					Nama Energy BOOST pertama kali diberikan karena teknologi pengembalian energi yang tinggi dan responsif, yang tercipta karena adanya foam BOOST di sepanjang sepatu pada sole dan midsole yang menyimpan dan mengembalikan energi ringan serta sangat cepat di setiap pijakan kaki.

					Tanpa mengubah setiap bagian yang membuat siluet ini unik, beberapa pembaharuan dan integrasi dilakukan, seperti midfoot construction yang disederhanakan dan dikombinasikan dengan cage yang lebih ringan untuk fit yang lebih nyaman, menjadikan versi ini sebuah evolusi yang sempurna dari versi original.
					
					"""
		)
		print 'create news 3 OK'

