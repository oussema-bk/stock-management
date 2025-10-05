from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import F
from products_app.models import Category, Product
from stock_app.models import StockLevel, StockMovement
from sales_app.models import Customer, Sale, SaleItem
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Clear and populate database with logical sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        
        # Clear all data (in correct order to avoid FK constraints)
        SaleItem.objects.all().delete()
        Sale.objects.all().delete()
        Customer.objects.all().delete()
        StockMovement.objects.all().delete()
        StockLevel.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('✓ Data cleared'))
        
        # Get or create admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin user created (username: admin, password: admin123)'))
        
        self.stdout.write('\nCreating sample data...\n')
        
        # Create Categories
        categories_data = [
            ('Résistances', 'Composants résistifs pour circuits électroniques'),
            ('Condensateurs', 'Condensateurs électrolytiques et céramiques'),
            ('LEDs', 'Diodes électroluminescentes de différentes couleurs'),
            ('Microcontrôleurs', 'Cartes de développement et microcontrôleurs'),
            ('Capteurs', 'Capteurs de température, mouvement, etc.'),
            ('Accessoires', 'Breadboards, câbles et autres accessoires'),
        ]
        
        categories = {}
        for name, desc in categories_data:
            cat = Category.objects.create(name=name, description=desc)
            categories[name] = cat
            self.stdout.write(f'  • Catégorie: {name}')
        
        # Create Products with logical pricing
        products_data = [
            # (name, sku, category, price, cost_price, description, initial_stock, min_stock)
            ('Résistance 10K Ohm', 'RES-10K', 'Résistances', 0.50, 0.25, 'Résistance 10K Ohm 1/4W 5%', 500, 100),
            ('Résistance 1K Ohm', 'RES-1K', 'Résistances', 0.50, 0.25, 'Résistance 1K Ohm 1/4W 5%', 450, 100),
            ('Résistance 220 Ohm', 'RES-220', 'Résistances', 0.50, 0.25, 'Résistance 220 Ohm 1/4W 5%', 600, 150),
            
            ('Condensateur 100uF 25V', 'CAP-100UF', 'Condensateurs', 1.20, 0.60, 'Condensateur électrolytique 100uF 25V', 200, 50),
            ('Condensateur 10uF 16V', 'CAP-10UF', 'Condensateurs', 0.80, 0.40, 'Condensateur électrolytique 10uF 16V', 250, 60),
            ('Condensateur 0.1uF', 'CAP-100NF', 'Condensateurs', 0.30, 0.15, 'Condensateur céramique 0.1uF 50V', 400, 100),
            
            ('LED Rouge 5mm', 'LED-RED-5MM', 'LEDs', 0.30, 0.15, 'LED rouge 5mm diffuse standard', 800, 200),
            ('LED Verte 5mm', 'LED-GREEN-5MM', 'LEDs', 0.30, 0.15, 'LED verte 5mm diffuse standard', 750, 200),
            ('LED Bleue 5mm', 'LED-BLUE-5MM', 'LEDs', 0.40, 0.20, 'LED bleue 5mm haute luminosité', 600, 150),
            ('LED RGB 5mm', 'LED-RGB-5MM', 'LEDs', 1.50, 0.75, 'LED RGB 5mm cathode commune', 300, 75),
            
            ('Arduino Uno R3', 'ARD-UNO', 'Microcontrôleurs', 25.00, 15.00, 'Carte Arduino Uno R3 ATmega328P', 50, 10),
            ('Arduino Nano', 'ARD-NANO', 'Microcontrôleurs', 18.00, 10.00, 'Carte Arduino Nano compatible', 75, 15),
            ('ESP32 DevKit', 'ESP32-DEV', 'Microcontrôleurs', 12.00, 7.00, 'Module ESP32 WiFi + Bluetooth', 100, 20),
            ('Raspberry Pi Pico', 'RPI-PICO', 'Microcontrôleurs', 8.00, 5.00, 'Raspberry Pi Pico RP2040', 80, 20),
            
            ('Capteur DHT11', 'SENS-DHT11', 'Capteurs', 3.50, 2.00, 'Capteur température et humidité', 120, 30),
            ('Capteur Ultrason HC-SR04', 'SENS-HCSR04', 'Capteurs', 2.50, 1.50, 'Capteur de distance ultrason', 150, 40),
            ('Capteur PIR', 'SENS-PIR', 'Capteurs', 2.00, 1.20, 'Capteur de mouvement infrarouge', 100, 25),
            
            ('Breadboard 830 points', 'BRD-830', 'Accessoires', 5.50, 3.00, 'Breadboard 830 points avec support', 75, 20),
            ('Câbles Jumper M/M x40', 'CABLE-MM-40', 'Accessoires', 2.50, 1.20, 'Pack 40 câbles jumper mâle-mâle', 150, 30),
            ('Câbles Jumper M/F x40', 'CABLE-MF-40', 'Accessoires', 2.50, 1.20, 'Pack 40 câbles jumper mâle-femelle', 140, 30),
        ]
        
        products = {}
        for data in products_data:
            name, sku, cat_name, price, cost, desc, stock, min_stock = data
            product = Product.objects.create(
                name=name,
                sku=sku,
                category=categories[cat_name],
                price=Decimal(str(price)),
                cost_price=Decimal(str(cost)),
                description=desc,
                is_active=True
            )
            products[sku] = product
            
            # Create stock level
            StockLevel.objects.create(
                product=product,
                current_stock=stock,
                minimum_stock=min_stock,
                maximum_stock=stock * 3
            )
            
            # Create initial stock IN movement
            StockMovement.objects.create(
                product=product,
                movement_type='IN',
                quantity=stock,
                reference='INIT-001',
                notes='Stock initial',
                created_by=admin_user
            )
            
            self.stdout.write(f'  • Produit: {name} (Stock: {stock})')
        
        # Create Customers
        customers_data = [
            ('TechSolutions SARL', 'contact@techsolutions.com', '0612345678', '15 Avenue des Technologies, Paris 75001'),
            ('ElectroMart', 'commandes@electromart.fr', '0623456789', '42 Rue de l\'Innovation, Lyon 69002'),
            ('MakerSpace Lyon', 'info@makerspace-lyon.fr', '0634567890', '8 Place des Makers, Lyon 69003'),
            ('Université Paris Tech', 'lab@paristech.edu', '0145678901', '25 Boulevard de la Science, Paris 75005'),
            ('Innovation Lab', 'contact@innovationlab.fr', '0656789012', '33 Rue du Progrès, Toulouse 31000'),
        ]
        
        customers = {}
        for name, email, phone, address in customers_data:
            customer = Customer.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address
            )
            customers[name] = customer
            self.stdout.write(f'  • Client: {name}')
        
        # Create sample sales (PENDING and COMPLETED)
        self.stdout.write('\n  Creating sales...')
        
        # Sale 1: COMPLETED - TechSolutions
        sale1 = Sale.objects.create(
            customer=customers['TechSolutions SARL'],
            status='PENDING',  # Will complete it
            created_by=admin_user
        )
        SaleItem.objects.create(
            sale=sale1,
            product=products['ARD-UNO'],
            quantity=5,
            unit_price=products['ARD-UNO'].price
        )
        SaleItem.objects.create(
            sale=sale1,
            product=products['LED-RED-5MM'],
            quantity=50,
            unit_price=products['LED-RED-5MM'].price
        )
        SaleItem.objects.create(
            sale=sale1,
            product=products['BRD-830'],
            quantity=3,
            unit_price=products['BRD-830'].price
        )
        sale1.complete_sale(admin_user)
        self.stdout.write(f'    ✓ Vente #{sale1.id} à {sale1.customer.name} - COMPLÉTÉE')
        
        # Sale 2: COMPLETED - ElectroMart
        sale2 = Sale.objects.create(
            customer=customers['ElectroMart'],
            status='PENDING',
            created_by=admin_user
        )
        SaleItem.objects.create(
            sale=sale2,
            product=products['RES-10K'],
            quantity=100,
            unit_price=products['RES-10K'].price
        )
        SaleItem.objects.create(
            sale=sale2,
            product=products['RES-1K'],
            quantity=100,
            unit_price=products['RES-1K'].price
        )
        SaleItem.objects.create(
            sale=sale2,
            product=products['CAP-100UF'],
            quantity=30,
            unit_price=products['CAP-100UF'].price
        )
        sale2.complete_sale(admin_user)
        self.stdout.write(f'    ✓ Vente #{sale2.id} à {sale2.customer.name} - COMPLÉTÉE')
        
        # Sale 3: PENDING - MakerSpace Lyon
        sale3 = Sale.objects.create(
            customer=customers['MakerSpace Lyon'],
            status='PENDING',
            created_by=admin_user
        )
        SaleItem.objects.create(
            sale=sale3,
            product=products['ESP32-DEV'],
            quantity=10,
            unit_price=products['ESP32-DEV'].price
        )
        SaleItem.objects.create(
            sale=sale3,
            product=products['SENS-DHT11'],
            quantity=8,
            unit_price=products['SENS-DHT11'].price
        )
        sale3.calculate_total()
        self.stdout.write(f'    ✓ Vente #{sale3.id} à {sale3.customer.name} - EN ATTENTE')
        
        # Sale 4: COMPLETED - Université
        sale4 = Sale.objects.create(
            customer=customers['Université Paris Tech'],
            status='PENDING',
            created_by=admin_user
        )
        SaleItem.objects.create(
            sale=sale4,
            product=products['RPI-PICO'],
            quantity=15,
            unit_price=products['RPI-PICO'].price
        )
        SaleItem.objects.create(
            sale=sale4,
            product=products['CABLE-MM-40'],
            quantity=20,
            unit_price=products['CABLE-MM-40'].price
        )
        sale4.complete_sale(admin_user)
        self.stdout.write(f'    ✓ Vente #{sale4.id} à {sale4.customer.name} - COMPLÉTÉE')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created successfully!'))
        self.stdout.write('\n📊 Summary:')
        self.stdout.write(f'  • Categories: {Category.objects.count()}')
        self.stdout.write(f'  • Products: {Product.objects.count()}')
        self.stdout.write(f'  • Customers: {Customer.objects.count()}')
        self.stdout.write(f'  • Sales: {Sale.objects.count()}')
        self.stdout.write(f'  • Completed Sales: {Sale.objects.filter(status="COMPLETED").count()}')
        self.stdout.write(f'  • Pending Sales: {Sale.objects.filter(status="PENDING").count()}')
        self.stdout.write(f'  • Stock Movements: {StockMovement.objects.count()}')
        self.stdout.write(f'  • Low Stock Products: {StockLevel.objects.filter(current_stock__lte=F("minimum_stock")).count()}')
