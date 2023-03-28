from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    class Meta:
        ordering = ['name', 'price']
        # Сортировка по имени, если написать '-name', то сортировка будет в обратном порядке.
        # Если будет совпадение по первому, то дальше будет сортировка по полю 'price'

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_ad = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)

    # @property
    # def description_short(self) -> str:    #если используется ТОЛЬКО для админки, то лучше перенести туда
    #     """Сокращает размер отображаемого поля с описанием"""
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48] + '...'

    def __str__(self) -> str:
        """Настройка отображения в навигационной панели"""
        return f'Product(pk={self.pk}, name={self.name!r})'


class Order(models.Model):
    delivery_adress = models.TextField(max_length=200, null=False, blank=False)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_ad = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')
