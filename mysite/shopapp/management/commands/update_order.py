from django.core.management import BaseCommand

from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.first()  # first - возьмет первую сущность, если ничего нет, то вернет none
        if not order:
            self.stdout.write('No orders found')
            return
        produst = Product.objects.all()

        for product in produst:
            order.products.add(product)

        order.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added to products {order.products.all()} to order {order}'
            )
        )
