from django.db import models


class HeroImageConf(models.Model):
	title = models.CharField(
			"Заголовок",
			null = True,
			blank = True,
			max_length = 100
		)
	enabled = models.BooleanField(default = False)

	def __str__(self):
		if self.title:
			return self.title
		return f"Unnamed {self.id}"

	class Meta:
		verbose_name = "Набор hero картинок"
		verbose_name_plural = "Наборы hero картинок"


class HeroImage(models.Model):
	hero_image_conf = models.ForeignKey(
			HeroImageConf,
			on_delete = models.SET_NULL,
			null = True
		)
	image = models.ImageField(
			"Картинка",
			upload_to = "hero_images/",
			null = True
		)
	enabled = models.BooleanField(default = True)