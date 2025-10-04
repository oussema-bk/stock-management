from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from decimal import Decimal
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
        for i in range(options['sales']):
            customer = random.choice(customers)
            sale = Sale.objects.create(
                customer=customer,
                status=random.choice(['COMPLETED', 'COMPLETED', 'COMPLETED', 'PENDING']),
                notes=fake.text(max_nb_chars=100),
                created_by=admin_user
            )
            
            # Add 1-5 items to each sale
            num_items = random.randint(1, 5)
            sale_products = random.sample(products, min(num_items, len(products)))
            
            for product in sale_products:
                quantity = random.randint(1, 10)
                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price
                )
            
            # Calculate total
            sale.calculate_total()
            
            # Update stock if sale is completed
            if sale.status == 'COMPLETED':
                for item in sale.sale_items.all():
                    stock_level = StockLevel.objects.get(product=item.product)
                    stock_level.current_stock -= item.quantity
                    stock_level.save()
                    
                    StockMovement.objects.create(
                        product=item.product,
                        movement_type='OUT',
                        quantity=item.quantity,
                        reference=f'SALE-{sale.id}',
                        notes=f'Sale to {customer.name}',
                        created_by=admin_user
                    )
        
        self.stdout.write(f'Created {options["sales"]} sales')
        
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
