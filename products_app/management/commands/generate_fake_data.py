from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
from decimal import Decimal
from datetime import timedelta
import random
from products_app.models import Category, Product
from stock_app.models import StockLevel, StockMovement
from sales_app.models import Customer, Sale, SaleItem

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake data for the electrical parts agency'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            type=int,
            default=10,
            help='Number of categories to create'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=50,
            help='Number of products to create'
        )
        parser.add_argument(
            '--customers',
            type=int,
            default=20,
            help='Number of customers to create'
        )
        parser.add_argument(
            '--sales',
            type=int,
            default=100,
            help='Number of sales to create'
        )

    def handle(self, *args, **options):
        self.stdout.write('Generating fake data...')
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Created admin user (username: admin, password: admin123)')
        
        # Get or create admin user
        admin_user = User.objects.get(username='admin')
        
        # Create categories
        self.stdout.write('Creating categories...')
        categories = []
        electrical_categories = [
            'Switches', 'Outlets', 'Lighting', 'Wiring', 'Circuit Breakers',
            'Transformers', 'Motors', 'Generators', 'Cables', 'Connectors',
            'Fuses', 'Relays', 'Sensors', 'Controllers', 'Inverters'
        ]
        
        for i in range(options['categories']):
            if i < len(electrical_categories):
                name = electrical_categories[i]
            else:
                name = fake.word().title() + ' Components'
            
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'description': fake.text(max_nb_chars=200),
                }
            )
            categories.append(category)
        
        self.stdout.write(f'Created {len(categories)} categories')
        
        # Create products
        self.stdout.write('Creating products...')
        products = []
        electrical_products = [
            'LED Light Bulb', 'Electrical Outlet', 'Light Switch', 'Circuit Breaker',
            'Electrical Wire', 'Power Cable', 'Extension Cord', 'Electrical Box',
            'Wire Nuts', 'Electrical Tape', 'Voltage Tester', 'Multimeter',
            'Electrical Panel', 'Ground Fault Outlet', 'Dimmer Switch',
            'Motion Sensor', 'Doorbell', 'Security Camera', 'Surge Protector',
            'Power Strip', 'Electrical Conduit', 'Junction Box', 'Wire Stripper',
            'Cable Ties', 'Electrical Connector', 'Fuse Box', 'Transformer',
            'Motor Starter', 'Relay Switch', 'Timer Switch', 'Photocell',
            'Electrical Receptacle', 'GFCI Outlet', 'USB Outlet', 'Smart Switch',
            'Electrical Fitting', 'Cable Gland', 'Terminal Block', 'Bus Bar',
            'Electrical Insulator', 'Power Meter', 'Energy Monitor', 'Smart Plug'
        ]
        
        for i in range(options['products']):
            if i < len(electrical_products):
                name = electrical_products[i]
            else:
                name = fake.word().title() + ' ' + fake.word().title()
            
            product = Product.objects.create(
                name=name,
                description=fake.text(max_nb_chars=300),
                sku=fake.bothify(text='ELEC-###-???'),
                category=random.choice(categories),
                price=Decimal(str(round(random.uniform(5.0, 500.0), 2))),
                cost_price=Decimal(str(round(random.uniform(2.0, 250.0), 2))),
                is_active=random.choice([True, True, True, False])  # 75% active
            )
            products.append(product)
        
        self.stdout.write(f'Created {len(products)} products')
        
        # Create stock levels
        self.stdout.write('Creating stock levels...')
        for product in products:
            stock_level = StockLevel.objects.create(
                product=product,
                current_stock=random.randint(0, 100),
                minimum_stock=random.randint(5, 20),
                maximum_stock=random.randint(50, 200)
            )
            
            # Create some stock movements
            if stock_level.current_stock > 0:
                StockMovement.objects.create(
                    product=product,
                    movement_type='IN',
                    quantity=stock_level.current_stock,
                    reference=fake.bothify(text='PO-###-???'),
                    notes='Initial stock',
                    created_by=admin_user
                )
        
        self.stdout.write('Created stock levels and movements')
        
        # Create customers
        self.stdout.write('Creating customers...')
        customers = []
        for i in range(options['customers']):
            customer = Customer.objects.create(
                name=fake.company(),
                email=fake.email(),
                phone=fake.phone_number(),
                address=fake.address()
            )
            customers.append(customer)
        
        self.stdout.write(f'Created {len(customers)} customers')
        
        # Create sales
        self.stdout.write('Creating sales...')
        completed_count = 0
        pending_count = 0
        failed_count = 0
        
        # Calculate date range (last 365 days)
        now = timezone.now()
        start_date = now - timedelta(days=365)
        
        for i in range(options['sales']):
            customer = random.choice(customers)
            
            # Generate random date within the last year
            random_days = random.randint(0, 365)
            sale_date = start_date + timedelta(days=random_days)
            
            # All sales start as PENDING
            sale = Sale.objects.create(
                customer=customer,
                status='PENDING',
                notes=fake.text(max_nb_chars=100),
                created_by=admin_user,
                sale_date=sale_date
            )
            
            # Add 1-5 items to each sale
            num_items = random.randint(1, 5)
            # Only use active products with stock
            available_products = [
                p for p in products 
                if p.is_active and hasattr(p, 'stock_level') and p.stock_level.current_stock > 0
            ]
            
            if not available_products:
                sale.delete()
                continue
            
            sale_products = random.sample(available_products, min(num_items, len(available_products)))
            
            for product in sale_products:
                # Limit quantity to available stock
                stock_level = StockLevel.objects.get(product=product)
                max_qty = min(10, stock_level.current_stock)
                if max_qty > 0:
                    quantity = random.randint(1, max_qty)
                    SaleItem.objects.create(
                        sale=sale,
                        product=product,
                        quantity=quantity,
                        unit_price=product.price
                    )
            
            # Calculate total
            sale.calculate_total()
            
            # Randomly complete 75% of sales, keep 25% pending
            should_complete = random.random() < 0.75
            
            if should_complete:
                try:
                    # Use the new automatic stock reduction method
                    sale.complete_sale(admin_user)
                    completed_count += 1
                except ValueError as e:
                    # If stock insufficient, keep as pending
                    pending_count += 1
            else:
                pending_count += 1
        
        self.stdout.write(f'Created sales: {completed_count} completed, {pending_count} pending')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated fake data:\n'
                f'- {len(categories)} categories\n'
                f'- {len(products)} products\n'
                f'- {len(customers)} customers\n'
                f'- {options["sales"]} sales\n'
                f'- Stock levels and movements\n\n'
                f'Admin user: admin / admin123'
            )
        )
