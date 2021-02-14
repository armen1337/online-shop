from django.urls import path

from . import views


urlpatterns = [
	path("", views.home, name="home"),
	path("cart/", views.cart, name="cart"),
	path("order=<str:transaction_id>", views.order_detail, name="order_detail"),
	path("checkout/", views.checkout, name="checkout"),

	# Code processing url's
	path("update_item/", views.update_item, name="update_item"),
	path("process_order/", views.process_order, name="process_order"),
]