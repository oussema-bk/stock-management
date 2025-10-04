from django.db import models
from django.core.validators import MinValueValidator
from products_app.models import Product


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJUSTMENT', 'Adjustment'),
        ('TRANSFER', 'Transfer'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    reference = models.CharField(max_length=100, blank=True)  # Invoice number, PO number, etc.
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()} ({self.quantity})"


class StockLevel(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock_level')
    current_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    minimum_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    maximum_stock = models.IntegerField(default=1000, validators=[MinValueValidator(1)])
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['product__name']
    
    def __str__(self):
        return f"{self.product.name} - {self.current_stock} units"
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock
    
    @property
    def is_out_of_stock(self):
        return self.current_stock == 0
    
    @property
    def stock_status(self):
        if self.is_out_of_stock:
            return 'Out of Stock'
        elif self.is_low_stock:
            return 'Low Stock'
        else:
            return 'In Stock'