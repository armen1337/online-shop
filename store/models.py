from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
	""" Клиент """
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length = 200, null=True)
	email = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Клиент"
		verbose_name_plural = "Клиенты"


class Product(models.Model):
	""" Продукт """
	name = models.CharField("Название", max_length=255, null=True)
	price = models.FloatField("Цена")
	image = models.ImageField("Картинка",upload_to="products/", null = True, blank = True)
	draft = models.BooleanField("Черновик",default = False)

	def __str__(self):
		return self.name

	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

	class Meta:
		verbose_name = "Продукт"
		verbose_name_plural = "Продукты"


class Order(models.Model):
	""" Заказ """
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add = True)
	complete = models.BooleanField(default = False)
	transaction_id = models.CharField(max_length = 200, null = True)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

	class Meta:
		verbose_name = "Заказ"
		verbose_name_plural = "Заказы"


class OrderItem(models.Model):
	""" Продукт при заказе """
	product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
	order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
	quantity = models.PositiveSmallIntegerField(default = 0, null = True, blank = True)
	date_added = models.DateTimeField(auto_now_add = True)

	@property
	def get_total(self):
		""" Возвращает общую сумму в корзине """
		total = self.product.price * self.quantity
		return total

	class Meta:
		verbose_name = "Продукт при заказе"
		verbose_name_plural = "Продукты при заказе"


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
	order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True, blank = True)
	address = models.CharField(max_length = 200, null = True)
	city = models.CharField(max_length = 200, null = True)
	zip_code = models.CharField(max_length = 200, null = True)
	date_added = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.address

	class Meta:
		verbose_name = "Адрес доставки"
		verbose_name_plural = "Адреса доставки"