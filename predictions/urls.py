from django.urls import path # type: ignore

from .views import prediction_detail_view, prediction_list_view

urlpatterns = [
    path('<slug:fixture_id>', prediction_detail_view, name='prediction_detail'),
    path('', prediction_list_view, name='prediction_list'),
]
