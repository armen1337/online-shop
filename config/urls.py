from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from register import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('store.urls')),
    path('register/', views.register_index, name="register"),
	path('', include("django.contrib.auth.urls")),
]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)