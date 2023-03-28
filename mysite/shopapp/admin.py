from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from .admin_mixin import ExportAsCSVMixin
from .models import Product, Order


class OrderInLine(admin.TabularInline):
    """Отображает список заказов, в продуктах"""
    model = Product.orders.through


@admin.action(description='Archive product')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive product')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


# admin.site.register(Product, ProductAdmin) #либо так, если без декоратора

@admin.register(Product)  # делает то же самое, что и закомменченая строчка ниже
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        'exports_csv'
    ]
    inlines = [
        OrderInLine
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'  # инф которая отображается
    list_display_links = 'pk', 'name'  # делает ссылками отображаемую инф
    ordering = 'pk', 'name'  # способ сортировки в админке, если добавить МИНУС, то будет в обратном порядке
    search_fields = 'name', 'price'  # поля по которым производить поиск
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        ('price_options', {
            'fields': ('price', 'discount'),
            'classes': ('wide', 'collapse',),
        }),
        ('extra_otpions', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Extra options. Field "archived" is for soft delete.'
        })
    ]

    def description_short(self, obj: Product):
        """Сокращает размер отображаемого поля с описанием в админку"""
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'


class ProductInLine(admin.TabularInline):  # Или StackedInline, разница только во внешнем виде отображения
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInLine
    ]

    list_display = 'delivery_adress', 'created_ad', 'promocode', 'user_verbose'

    def get_queryset(self, request):
        """Оптимизирует запросы, когда на странице будет много заказов,
         пользователи будут подгружаться в рамках одного запроса,
          а не для каждого заказа отдельно"""
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        """возвращает имя, если его нет - имя пользователя, для отображения"""
        return obj.user.first_name or obj.user.username
