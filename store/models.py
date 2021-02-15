from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save


class Category(models.Model):
	""" Category and subcategory (that can
	be accessed with related name below) """
	parent = models.ForeignKey(
			'self',
			related_name = 'children',
			on_delete = models.CASCADE,
			blank = True,
			null = True
		)
	name = models.CharField(
			"Название (30 макс.)",
			max_length=30,
			unique = True
		)
	url = models.SlugField("URL", unique = True, blank = True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Категория"
		verbose_name_plural = "Категории"


class Customer(models.Model):
	""" Customer """
	user = models.OneToOneField(
			User,null = True,
			blank = True,
			on_delete = models.CASCADE
		)
	name = models.CharField(max_length = 200, null=True)
	email = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Клиент"
		verbose_name_plural = "Клиенты"


class Product(models.Model):
	""" Product """
	name = models.CharField("Название", max_length = 255, null = True)
	price = models.DecimalField("Цена", max_digits = 7, decimal_places = 2)
	image = models.ImageField(
			"Картинка",
			upload_to = "products/",
			null = True,
			blank = True
		)
	draft = models.BooleanField("Черновик", default = False)
	category = models.ForeignKey(
			Category,
			related_name = 'products',
			on_delete = models.SET_NULL,
			null = True
		)

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


class Status(models.Model):
	name = models.CharField("Статус", max_length = 100)
	value = models.SlugField(
			"Value",
			max_length = 20,
			null = True,
			blank = True,
		)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Статус заказа"
		verbose_name_plural = "Статусы заказа"


class Order(models.Model):
	""" If order's complete parameter is false,
	then the order is in "cart" condition.
	"""
	customer = models.ForeignKey(
			Customer,
			on_delete = models.SET_NULL,
			null = True,
			blank = True
		)
	date_ordered = models.DateTimeField(auto_now_add = True)
	complete = models.BooleanField(default = False)
	transaction_id = models.CharField(
			max_length = 200,
			null = True,
			blank = True)
	status = models.ForeignKey(
			Status,
			null = True,
			blank = True,
			on_delete = models.SET_NULL,
		)

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

	def get_absolute_url(self):
		return "order={}".format(self.transaction_id)

	class Meta:
		verbose_name = "Заказ"
		verbose_name_plural = "Заказы"


class OrderItem(models.Model):
	""" Same "Product" model but with capacity
	of changing the quantity.
	"""
	product = models.ForeignKey(
			Product,
			on_delete = models.SET_NULL,
			null = True
		)
	order = models.ForeignKey(
			Order,
			on_delete = models.SET_NULL,
			null = True
		)
	quantity = models.PositiveSmallIntegerField(
			default = 0,
			null = True,
			blank = True
		)
	date_added = models.DateTimeField(auto_now_add = True)

	@property
	def get_total(self):
		""" Возвращает общую сумму в корзине """
		total = self.product.price * self.quantity
		return total

	def __str__(self):
		return self.product.name

	class Meta:
		verbose_name = "Заказанный продукт"
		verbose_name_plural = "Заказанные продукты"


class ShippingAddress(models.Model):
	""" Shipping address of customer """
	customer = models.ForeignKey(
			Customer,
			on_delete = models.SET_NULL,
			null = True,
			blank = True
		)
	order = models.ForeignKey(
			Order,
			on_delete = models.SET_NULL,
			null = True,
			blank = True
		)
	address = models.CharField(max_length = 200, null = True)
	city = models.CharField(max_length = 200, null = True)
	zip_code = models.CharField(max_length = 200, null = True)
	date_added = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.address

	class Meta:
		verbose_name = "Адрес доставки"
		verbose_name_plural = "Адреса доставки"


def create_slug(instance, new_slug = None):
	""" Generates a slug for Category object """
	slug = instance.name.lower().replace(' ', '-')
	if new_slug is not None:
		slug = new_slug

	queryset = Category.objects.filter(url=slug).order_by("-id")

	if queryset.exists():
		new_slug = "%s-%s"%(slug, queryset.first().id)
		return create_slug(instance, new_slug = new_slug)
	return slug


def pre_save_category(sender, instance, *args, **kwargs):
	if not instance.url:
		instance.url = create_slug(instance)


pre_save.connect(pre_save_category, Category)