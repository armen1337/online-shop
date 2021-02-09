from django.shortcuts import render, redirect
from django.http import JsonResponse

import json
import datetime

from .models import Product, Order, OrderItem, ShippingAddress
from .utils import get_order_and_items


def home(request):
	products = Product.objects.all()
	cartItems = get_order_and_items(request)["cartItems"]

	context = {
		"products": products,
		"cartItems": cartItems,
	}
	return render(request, "store/home.html", context)


def cart(request):
	order_and_items = get_order_and_items(request)
	
	context = {
		"items": order_and_items["items"],
		"order": order_and_items["order"],
	}
	return render(request, "store/cart.html", context)


def checkout(request):
	if not request.user.is_authenticated:
		return redirect("home")
	order_and_items = get_order_and_items(request)

	context = {
		"items": order_and_items["items"],
		"order": order_and_items["order"],
	}
	return render(request, "store/checkout.html", context)


def update_item(request):
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

	return JsonResponse("Item was added", safe=False)


def process_order(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float( data["form"]["total"].replace(',', '.') )
		order.transaction_id = transaction_id

		if float(total) == float(order.get_cart_total):
			order.complete = True

		order.save()

		ShippingAddress.objects.create(
				customer = customer,
				order = order,
				address = data["shipping"]["address"],
				city = data["shipping"]["city"],
				zip_code = data["shipping"]["zipcode"],
			)

	else:
		print("User is not logged in..")


	return JsonResponse("Payment complete!", safe=False)