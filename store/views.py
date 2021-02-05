from django.shortcuts import render
from django.http import JsonResponse
import json

from .models import Product, Order, OrderItem
from .store_services import get_order_and_items


def store(request):
	products = Product.objects.all()
	order, items = get_order_and_items(request)
	cartItems = get_order_and_items(request, getCartItems = True)
	print(cartItems)
	context = {
		"products": products,
		"cartItems": cartItems,
	}
	return render(request, "store/store.html", context)


def cart(request):
	order, items = get_order_and_items(request)
	context = {
		"items": items,
		"order": order,
	}
	return render(request, "store/cart.html", context)


def checkout(request):
	order, items = get_order_and_items(request)
	context = {
		"items": items,
		"order": order,
	}
	return render(request, "store/checkout.html", context)


def update_item(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print("Action:", action)
	print("Product ID:", productId)

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