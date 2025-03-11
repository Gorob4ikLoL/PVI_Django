from django.shortcuts import render, get_object_or_404, redirect
from .models import Instrument, Order
from django.contrib import messages
from django import forms


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'customer_name', 'customer_email']


def instrument_list(request):
    instruments = Instrument.objects.all()
    return render(request, 'instruments/instrument_list.html', {'instruments': instruments})


def instrument_detail(request, instrument_id):
    instrument = get_object_or_404(Instrument, pk=instrument_id)
    return render(request, 'instruments/instrument_detail.html', {'instrument': instrument})


def create_order(request, instrument_id):
    instrument = get_object_or_404(Instrument, pk=instrument_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.instrument = instrument

            # Перевірка наявності потрібної кількості на складі
            if order.quantity <= instrument.stock_quantity:
                # Зменшення кількості на складі
                instrument.stock_quantity -= order.quantity
                instrument.save()

                order.save()
                messages.success(request, 'Замовлення успішно створено!')
                return redirect('instruments:instrument_list')
            else:
                messages.error(request, 'На складі недостатньо товару!')
    else:
        form = OrderForm()

    return render(request, 'instruments/create_order.html', {
        'form': form,
        'instrument': instrument
    })