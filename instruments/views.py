from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view

from .models import Instrument, Order
from django.contrib import messages
from django import forms
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InstrumentSerializer, UserRegistrationSerializer
from .permissions import IsAdmin
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


@api_view(['GET', 'POST'])
def register_user(request):
    if request.method == 'GET':
        return Response({
            'message': 'Надішліть POST-запит з імʼям користувача, email та паролем для реєстрації.'
        })

    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"message": "Це сторінка для адміністраторів."})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Користувач з таким імʼям вже існує.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Реєстрація успішна! Тепер увійдіть.')
            return redirect('login')  # або будь-яка сторінка після реєстрації

    return render(request, 'users/register.html')