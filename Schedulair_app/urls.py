from django.urls import include, path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("home/", home),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)