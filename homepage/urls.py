from django.urls import path # type: ignore

from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.home, name='home'),
]