from django.urls import path
from . import views

app_name = 'instruments'

urlpatterns = [
    path('', views.instrument_list, name='instrument_list'),
    path('instrument/<int:instrument_id>/', views.instrument_detail, name='instrument_detail'),
    path('order/<int:instrument_id>/', views.create_order, name='create_order'),
]