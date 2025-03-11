from django.db import models


class Instrument(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    stock_quantity = models.IntegerField(verbose_name="Кількість на складі")
    instrument_type = models.CharField(max_length=50, verbose_name="Тип інструменту")
    image = models.ImageField(upload_to='instruments/', verbose_name="Фото", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Інструмент"
        verbose_name_plural = "Інструменти"


class Order(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, verbose_name="Інструмент")
    quantity = models.IntegerField(verbose_name="Кількість")
    customer_name = models.CharField(max_length=100, verbose_name="Ім'я клієнта")
    customer_email = models.EmailField(verbose_name="Електронна пошта клієнта")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата замовлення")

    def __str__(self):
        return f"Замовлення {self.id} - {self.customer_name}"

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"