from django import forms
from django.core import validators
from .models import Product, Order
from django.contrib.auth.models import Group


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'description', 'price', 'discount',


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=1000000, decimal_places=2)
#     description = forms.CharField(
#         widget=forms.Textarea(attrs={
#             'rows': 5,
#             'cols': 30
#         }),  # с помощью 'attrs' можно передать необходимы параметры, например кол-во колонок и строк при отрисовки поля
#         label='Product description',
#         validators=[validators.RegexValidator(
#             regex=r'great',  # слово которое должно содержаться в описании
#             message='Field must contain word "great"'  # текст ошибки
#         )],
#     )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'user', 'products', 'delivery_adress', 'promocode'


class GroupForms(forms.ModelForm):
    class Meta:
        model = Group
        fields = 'name',
