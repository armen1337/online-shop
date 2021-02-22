from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import HeroImage, HeroImageConf


class HeroImageInline(admin.StackedInline):
	model = HeroImage
	extra = 1
	readonly_fields = ("get_image",)

	fields = ("image", "get_image", "enabled")

	def get_image(self, obj):
		return mark_safe(f"""<img src="{obj.image.url}"
			width="400px">""")

	get_image.short_description = "Обзор"

	verbose_name = "Картинка hero"
	verbose_name_plural = "Картинки"


@admin.register(HeroImageConf)
class HeroImageConf(admin.ModelAdmin):
	model = HeroImageConf
	list_display = ("__str__", "enabled")
	list_editable = ("enabled",)


	inlines = [HeroImageInline]

	fields = ("title", "enabled")