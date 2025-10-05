from django.core.management.base import BaseCommand
from products_app.models import Category, Product
from stock_app.models import StockLevel, StockMovement
from sales_app.models import Customer, Sale, SaleItem


class Command(BaseCommand):
    help = 'Delete all data except users'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting all data (keeping users)...')
        
        # Delete in correct order to avoid FK constraints
        deleted_counts = {}
        
        deleted_counts['SaleItems'] = SaleItem.objects.all().delete()[0]
        deleted_counts['Sales'] = Sale.objects.all().delete()[0]
        deleted_counts['Customers'] = Customer.objects.all().delete()[0]
        deleted_counts['StockMovements'] = StockMovement.objects.all().delete()[0]
        deleted_counts['StockLevels'] = StockLevel.objects.all().delete()[0]
        deleted_counts['Products'] = Product.objects.all().delete()[0]
        deleted_counts['Categories'] = Category.objects.all().delete()[0]
        
        self.stdout.write(self.style.SUCCESS('\n✅ Data deleted successfully!\n'))
        self.stdout.write('Deleted:')
        for model, count in deleted_counts.items():
            self.stdout.write(f'  • {model}: {count}')
        
        self.stdout.write(self.style.WARNING('\n⚠️  Users were preserved'))
