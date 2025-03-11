from django.contrib import admin

from django.contrib import admin
from .models import Instrument, Order

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'instrument_type', 'price', 'stock_quantity')
    list_filter = ('instrument_type',)
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'instrument', 'quantity', 'customer_name', 'customer_email', 'order_date')
    list_filter = ('order_date',)
    search_fields = ('customer_name', 'customer_email')