from django.urls import path # type: ignore

from .views import m_and_a_view


urlpatterns = [
    path('', m_and_a_view, name='m_and_a'),
]