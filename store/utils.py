from django.core.exceptions import ObjectDoesNotExist

import json
from random import randint

from .models import (Order, Product, Customer,
	ShippingAddress, Status, OrderItem)


def get_order_and_items(request):
	""" Returns an order and a list of cart items
	Also, if user is authenticated, then it will
	return "order", "items" and "cartItems" from database
	normally, but if user is not authenticated,
	then it will deal with cookies.
	"""
	if request.user.is_authenticated:
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


def order_processing(request, json_data, transaction_id):
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	total = float( json_data["form"]["total"].replace(',', '.') )
	order.transaction_id = transaction_id + str(randint(1000,5000))

	if float(total) == float(order.get_cart_total):
		status = Status.objects.first()
		order.complete = True
		order.status = status
		order.save()


	ShippingAddress.objects.create(
			customer = customer,
			order = order,
			address = json_data["shipping"]["address"],
			city = json_data["shipping"]["city"],
			zip_code = json_data["shipping"]["zipcode"],
		)


def item_updating(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == "add":
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == "remove":
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()