from django.contrib import admin

from .models import (Category, Customer, Product, Order,
	OrderItem, ShippingAddress)


admin.site.site_title = "Онлайн магазин"
admin.site.site_header = "Онлайн магазин"


admin.site.register(ShippingAddress)


class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0
	classes = ("collapse",)

	readonly_fields = ('product', 'quantity', "date_added")

	fieldsets = (
		(None, {
				"fields": (("product"), ("quantity"), ("date_added") )
			}),
	)


class ShippingAddressInline(admin.StackedInline):
	model = ShippingAddress
	extra = 0
	classes = ("collapse",)
	add_form_template = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	model = Order

	# save_on_top = True

	list_filter = ("complete",)
	list_display = ("id", "customer", "complete")
	list_display_links = ("id", "customer")

	readonly_fields = ("date_ordered",)

	inlines = [ShippingAddressInline, OrderItemInline]

	fieldsets = (
		("Информация о заказе", {
				"fields": (
						("customer"),
						("date_ordered"),
						("complete"),
						("transaction_id"),
						("confirmed")
					)
			}),
	)

class CategoryInline(admin.StackedInline):
	model = Category
	extra = 1
	classes = ("collapse",)
	verbose_name = "Подкатегория"
	verbose_name_plural = "Подкатегории"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	model = Category

	inlines = [CategoryInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "price", "category", "draft")
	list_editable = ("draft",)