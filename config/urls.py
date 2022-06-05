from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from django.conf.urls import include # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
]
