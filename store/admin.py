from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Category, Customer, Product, Order,
	OrderItem, ShippingAddress, Status)


admin.site.site_header = "Онлайн магазин"
admin.site.site_title = "Онлайн магазин"
admin.site.index_title = "Администрирование онлайн магазина"

# unimportant
# admin.site.register(ShippingAddress)

# DELETE feature of adding items for inline blocks

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

	readonly_fields = (
			'product',
			'quantity',
			"date_added",
			"get_total_price",
			"get_product_id"
		)

	fields =  (
			"product",
			"get_product_id",
			"quantity",
			# "date_added",
			"get_total_price"
		)

	def get_total_price(self, obj):
		return f"${obj.get_total}"

	def get_product_id(self, obj):
		return obj.product.id

	get_total_price.short_description = "Итоговая цена"
	get_product_id.short_description = "ID продукта"


class ShippingAddressInline(admin.StackedInline):
	model = ShippingAddress
	extra = 0
	classes = ('collapse',)
	add_form_template = False

	readonly_fields = (
			"customer",
			"address",
			"city",
			"zip_code",
			"date_added"
		)

	fields = (
			"address",
			"city",
			"zip_code",
		)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
	model = Status

	list_display = ("id", "name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	model = Order

	# save_on_top = True

	search_fields = ("customer__name", "id", "transaction_id")

	list_filter = ("complete", "status")
	list_display = (
			"id",
			"customer",
			"complete",
			"status",
			"date_ordered",
		)
	list_display_links = ("id", "customer")

	readonly_fields = (
			"date_ordered",
			"complete",
			"transaction_id",
			"customer",
			"get_cart_total_price"
		)

	inlines = [ShippingAddressInline, OrderItemInline]

	fieldsets = (
		("Информация о заказе", {
				"fields": (
						("customer"),
						("date_ordered"),
						("complete"),
						("transaction_id"),
						("status"),
						("get_cart_total_price")
					)
			}),
	)


	def get_cart_total_price(self, obj):
		return f"${obj.get_cart_total}"

	get_cart_total_price.short_description = "Итоговая цена"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	model = Category

	inlines = [CategoryInline]

	fields = ("parent", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = (
			"id",
			"name",
			"price",
			"get_absolute_price_in_list",
			"category",
			"get_image",
			"draft"
		)

	list_display_links = ("id", "name")
	list_editable = ("draft",)

	search_fields = ("name", "id")
	readonly_fields = (
			"get_larger_image",
			"get_absolute_price",
			"get_absolute_price_in_list"
		)

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
		return mark_safe(f'<img src="{obj.image.url}" width="70" height="60">')

	def get_larger_image(self, obj):
		return mark_safe(f"""<img src="{obj.image.url}" width="200" height="170"
			style="border: 1px solid gray; padding: 4px;">""")

	def get_absolute_price(self, obj):
		return f"${obj.get_price}"

	def get_absolute_price_in_list(self, obj):
		return f"${obj.get_price} ({obj.discount}%)"


	get_image.short_description = "Картинка"
	get_larger_image.short_description = "Картинка"
	get_absolute_price.short_description = "Цена в скидке"
	get_absolute_price_in_list.short_description = "Цена в скидке"