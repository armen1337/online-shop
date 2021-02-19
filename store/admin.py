from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Category, Customer, Product, Order,
	OrderItem, ShippingAddress, Status)


admin.site.site_header = "Онлайн магазин"
admin.site.site_title = "Онлайн магазин"
admin.site.index_title = "Администрирование онлайн магазина"


admin.site.register(ShippingAddress)


class CategoryInline(admin.StackedInline):
	model = Category
	extra = 1
	classes = ("collapse",)
	verbose_name = "Подкатегория"
	verbose_name_plural = "Подкатегории"
	fields = ("name",)


class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0
	classes = ('collapse',)

	readonly_fields = ('product', 'quantity', "date_added")

	fieldsets = (
		(None, {
				"fields": (("product"), ("quantity"), ("date_added") )
			}),
	)


class ShippingAddressInline(admin.StackedInline):
	model = ShippingAddress
	extra = 0
	classes = ('collapse',)
	add_form_template = False


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
	model = Status

	list_display = ("id", "name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	model = Order

	# save_on_top = True

	list_filter = ("complete", "status")
	list_display = ("id", "customer", "complete", "status", "date_ordered")
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	model = Category

	inlines = [CategoryInline]

	fields = ("parent", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = (
			"name",
			"price",
			"get_absolute_price",
			"category",
			"get_image",
			"draft"
		)
	list_editable = ("draft",)

	readonly_fields = ("get_larger_image", "get_absolute_price")

	fields = (
			"name",
			"price",
			"get_larger_image",
			"image",
			"category",
			"draft",
			"discount",
			"get_absolute_price"
		)


	def get_image(self, obj):
		""" Постер в списке фильмов """
		return mark_safe(f'<img src="{obj.image.url}" width="70" height="60">')

	def get_larger_image(self, obj):
		""" Постер в списке фильмов """
		return mark_safe(f"""<img src="{obj.image.url}" width="200" height="170"
			style="border: 1px solid gray; padding: 4px;">""")

	def get_absolute_price(self, obj):
		return f"${obj.get_price}"


	get_image.short_description = "Картинка"
	get_larger_image.short_description = "Картинка"
	get_absolute_price.short_description = "Цена в скидке"