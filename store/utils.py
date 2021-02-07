from django.core.exceptions import ObjectDoesNotExist

import json

from .models import Order, Product


def get_order_and_items(request):
	""" Возвращает заказ и список товаров """
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items

	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
		items = []
		order = {"get_cart_total": 0, "get_cart_items": 0,}
		cartItems = order["get_cart_items"]

		for i in cart:
			try:
				product = Product.objects.get(id=i)

			except ObjectDoesNotExist as DoesNotExist:
				continue

			cartItems += cart[i]["quantity"]

			total = product.price * cart[i]["quantity"]

			order["get_cart_total"] += total
			order["get_cart_items"] += cart[i]["quantity"]

			item = {
				"product": {
					"id": product.id,
					"name": product.name,
					"price": product.price,
					"imageURL": product.imageURL,
					"draft": product.draft
					},
				"quantity": cart[i]["quantity"],
				"get_total": total
				}

			items.append(item)

	return {
		"order": order,
		"items": items,
		"cartItems": cartItems
	}