from django.urls import include, path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("dashboard/", dashboard),
    # path("login/", loginpage, name="login_page")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)