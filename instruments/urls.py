from django.urls import path
from . import views

app_name = 'instruments'

urlpatterns = [
    # 🌐 HTML-сторінки
    path('', views.instrument_list, name='instrument_list'),
    path('instrument/<int:instrument_id>/', views.instrument_detail, name='instrument_detail'),
    path('instrument/<int:instrument_id>/order/', views.create_order, name='create_order'),

    # 🔌 API endpoints
    path('api/instruments/', views.InstrumentList.as_view(), name='api_instrument_list'),
    path('api/instruments/<int:pk>/', views.InstrumentDetail.as_view(), name='api_instrument_detail'),
]
