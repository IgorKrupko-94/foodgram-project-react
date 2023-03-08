from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from backend.foodgram.foodgram import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
