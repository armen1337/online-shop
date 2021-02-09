from django.contrib import admin

from .models import (Customer, Product, Order,
	OrderItem, ShippingAddress)


admin.site.site_title = "Онлайн магазин"
admin.site.site_header = "Онлайн магазин"

# admin.site.register(OrderItem)

admin.site.register(Product)
admin.site.register(ShippingAddress)


class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0

	readonly_fields = ('product', 'quantity', "date_added")

	fieldsets = (
		(None, {
				"fields": (("product"), ("quantity"), ("date_added") )
			}),
	)


class ShippingAddressInline(admin.StackedInline):
	model = ShippingAddress
	extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	model = Customer

	fieldsets = (
		(None, {
				"fields": (("user"), ("name"), ("email"), )
			}),
	)

	def get_orders_count(self):
		return len(self.order_set.all()) # error


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	model = Order

	list_filter = ("complete",)
	list_display = ("id", "customer", "complete")

	readonly_fields = ("date_ordered",)

	inlines = [OrderItemInline]

	fieldsets = (
		("Информация о заказе", {
				"fields": (("customer"), ("date_ordered"), ("complete"), ("transaction_id") )
			}),
	)

