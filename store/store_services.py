from .models import Order


def get_order_and_items(request, getCartItems = False):
	""" Возвращает заказ и список товаров """
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {"get_cart_total": 0, "get_cart_items": 0,}
		cartItems = order["get_cart_items"]

	if getCartItems:
		return cartItems
	return order, items