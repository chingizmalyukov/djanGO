from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    """create product"""

    def handle(self, *args, **options):
        self.stdout.write('Create products')
        products_names = [
            'Desktop',
            'Laptop',
            'Smartphone'
        ]
        for products_name in products_names:
            product, created = Product.objects.get_or_create(name=products_name)
            self.stdout.write(f'Created product {products_name}')
        self.stdout.write(self.style.SUCCESS('Products created!'))
