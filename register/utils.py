from store.models import Customer, Order, Product

import json


def load_cookies_to_user_cart(request):
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		return None

	try:
		customer = request.user.customer
	except:
		customer = Customer.objects.create(
				user = request.user,
				name = request.user.username,
				email = request.user.email
			)
		customer.save()

	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	"""
	In for cycle the 'i' iteratior is productId, while the quantity
	can be accessed by typing 'cart[i]["quantity"]'
	"""
	for i in cart:
		try:
			product = Product.objects.get(id = int(i) )
		except:
			continue

		quantity = int(cart[i]["quantity"])

		order.orderitem_set.create(
				product = product,
				order = order,
				quantity = quantity
			)

