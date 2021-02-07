from django import template

from store.models import Order
from store.utils import get_order_and_items


register = template.Library()

@register.simple_tag()
def get_items_in_cart(request):
	cartItems = get_order_and_items(request)["cartItems"]
	return cartItems