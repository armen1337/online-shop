from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Category, Customer, Product, Order,
	OrderItem, ShippingAddress, Status)

# Grappelli customisation - https://django-grappelli.readthedocs.io/en/latest/customization.html

admin.site.register(Status)
admin.site.register(ShippingAddress)


class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0
	classes = ('grp-collapse grp-closed',)

	readonly_fields = ('product', 'quantity', "date_added")

	fieldsets = (
		(None, {
				"fields": (("product"), ("quantity"), ("date_added") )
			}),
	)


class ShippingAddressInline(admin.StackedInline):
	model = ShippingAddress
	extra = 0
	classes = ('grp-collapse',)
	add_form_template = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	model = Order

	# save_on_top = True

	list_filter = ("complete", "status")
	list_display = ("id", "customer", "complete", "status")
	list_display_links = ("id", "customer")

	readonly_fields = (
			"date_ordered",
			"complete",
			"transaction_id",
			"customer"
		)

	inlines = [ShippingAddressInline, OrderItemInline]

	fieldsets = (
		("Информация о заказе", {
				"fields": (
						("customer"),
						("date_ordered"),
						("complete"),
						("transaction_id"),
						("status")
					)
			}),
	)

class CategoryInline(admin.StackedInline):
	model = Category
	extra = 1
	classes = ("collapse",)
	verbose_name = "Подкатегория"
	verbose_name_plural = "Подкатегории"
	fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	model = Category

	inlines = [CategoryInline]

	fields = ("parent", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "price", "category", "get_image", "draft")
	list_editable = ("draft",)


	def get_image(self, obj):
		""" Постер в списке фильмов """
		return mark_safe(f'<img src="{obj.imageURL}" width="50" height="60">')