from django.urls import path # type: ignore

from .views import contact_view


urlpatterns = [
    path('', contact_view, name='contact'),
]