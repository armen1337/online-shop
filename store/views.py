from django.shortcuts import render, redirect
from django.http import JsonResponse

import json
import datetime

from .models import Product, Order, OrderItem, ShippingAddress
from .utils import (get_order_and_items,
	order_processing, item_updating)
from main.models import HeroImageConf


def home(request):
	products = Product.objects.all()
	cartItems = get_order_and_items(request)["cartItems"]

	if request.user.is_authenticated:
		orders = Order.objects.filter(customer = request.user.customer)

		is_any_complete = False
		for order in orders:
			if order.complete:
				is_any_complete = True
				break
	else:
		orders = []
		is_any_complete = False


	hero_image_conf = HeroImageConf.objects.filter(enabled = True).first()
	try:
		hero_images = hero_image_conf.heroimage_set.all()
	except:
		hero_images = None

	context = {
		"products": products,
		"cartItems": cartItems,
		"orders": orders,
		"is_any_complete": is_any_complete,

		"hero_images": hero_images
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
	if not request.user.is_authenticated: # or cart is empty
		return redirect("home")

	order_and_items = get_order_and_items(request)

	order = order_and_items["order"]

	if len(order.orderitem_set.all()) == 0:
		return redirect("home")

	context = {
		"items": order_and_items["items"],
		"order": order,
	}
	return render(request, "store/checkout.html", context)


def update_item(request):
	""" Updates an item quantity in cart.
	If an item quantity reaches 0, the item
	is automatically removed from the cart.
	"""
	item_updating(request)

	return JsonResponse("Item was added", safe=False)


def process_order(request):
	transaction_id = str(datetime.datetime.now().timestamp()).replace(".", "")
	data = json.loads(request.body)

	if request.user.is_authenticated:
		order_processing(request, data, transaction_id)

	return JsonResponse("Payment complete!", safe=False)


def order_detail(request, transaction_id):
	order = Order.objects.get(transaction_id=transaction_id)

	context = {
		"order": order,
	}
	return render(request, "store/order_detail.html", context)