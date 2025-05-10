from django.shortcuts import render, get_object_or_404, redirect
from .models import Instrument, Order
from django.contrib import messages
from django import forms
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InstrumentSerializer


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
class InstrumentList(APIView):
    def get(self, request):
        instruments = Instrument.objects.all()
        serializer = InstrumentSerializer(instruments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InstrumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstrumentDetail(APIView):
    def get(self, request, pk):
        instrument = get_object_or_404(Instrument, pk=pk)
        serializer = InstrumentSerializer(instrument)
        return Response(serializer.data)

    def put(self, request, pk):
        instrument = get_object_or_404(Instrument, pk=pk)
        serializer = InstrumentSerializer(instrument, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instrument = get_object_or_404(Instrument, pk=pk)
        instrument.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)