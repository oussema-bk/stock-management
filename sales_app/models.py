from django.db import models
from django.core.validators import MinValueValidator
from django.db import transaction
from products_app.models import Product
from decimal import Decimal


class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    address = models.TextField(blank=True, verbose_name="Adresse")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Sale(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('COMPLETED', 'Terminée'),
        ('CANCELLED', 'Annulée'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales', verbose_name="Client")
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de vente")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Statut")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Montant total")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Créé par")
    
    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        ordering = ['-sale_date']
    
    def __str__(self):
        return f"Vente #{self.id} - {self.customer.name} ({self.sale_date.strftime('%Y-%m-%d')})"
    
    def calculate_total(self):
        total = sum(item.line_total for item in self.sale_items.all())
        self.total_amount = total
        self.save()
        return total
    
    def complete_sale(self, user):
        """Complete the sale and reduce stock"""
        from stock_app.models import StockLevel, StockMovement
        
        if self.status == 'COMPLETED':
            return  # Already completed
        
        with transaction.atomic():
            for item in self.sale_items.all():
                stock_level = StockLevel.objects.filter(product=item.product).first()
                if not stock_level or stock_level.current_stock < item.quantity:
                    raise ValueError(
                        f'Stock insuffisant pour {item.product.name}'
                    )
                
                # Reduce stock
                stock_level.current_stock -= item.quantity
                stock_level.save()
                
                # Create stock movement
                StockMovement.objects.create(
                    product=item.product,
                    movement_type='OUT',
                    quantity=item.quantity,
                    reference=f'Vente #{self.id}',
                    notes=f'Vente à {self.customer.name}',
                    created_by=user
                )
            
            self.status = 'COMPLETED'
            self.save()
    
    def cancel_sale(self, user):
        """Cancel the sale and restore stock"""
        from stock_app.models import StockLevel, StockMovement
        
        if self.status != 'COMPLETED':
            self.status = 'CANCELLED'
            self.save()
            return
        
        with transaction.atomic():
            for item in self.sale_items.all():
                stock_level = StockLevel.objects.filter(product=item.product).first()
                if stock_level:
                    # Restore stock
                    stock_level.current_stock += item.quantity
                    stock_level.save()
                    
                    # Create stock movement
                    StockMovement.objects.create(
                        product=item.product,
                        movement_type='IN',
                        quantity=item.quantity,
                        reference=f'Annulation Vente #{self.id}',
                        notes=f'Annulation vente à {self.customer.name}',
                        created_by=user
                    )
            
            self.status = 'CANCELLED'
            self.save()


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_items', verbose_name="Vente")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Quantité")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Prix unitaire")
    
    class Meta:
        verbose_name = "Article de vente"
        verbose_name_plural = "Articles de vente"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def line_total(self):
        if self.quantity is not None and self.unit_price is not None:
            return self.quantity * self.unit_price
        return Decimal('0.00')