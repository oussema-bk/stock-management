from django.db import models
from django.core.validators import MinValueValidator
from products_app.models import Product


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Entrée de stock'),
        ('OUT', 'Sortie de stock'),
        ('ADJUSTMENT', 'Ajustement'),
        ('TRANSFER', 'Transfert'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements', verbose_name="Produit")
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES, verbose_name="Type de mouvement")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Quantité")
    reference = models.CharField(max_length=100, blank=True, verbose_name="Référence")  # Invoice number, PO number, etc.
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Créé par")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()} ({self.quantity})"


class StockLevel(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock_level', verbose_name="Produit")
    current_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Stock actuel")
    minimum_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Stock minimum")
    maximum_stock = models.IntegerField(default=1000, validators=[MinValueValidator(1)], verbose_name="Stock maximum")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    class Meta:
        verbose_name = "Niveau de stock"
        verbose_name_plural = "Niveaux de stock"
        ordering = ['product__name']
    
    def __str__(self):
        return f"{self.product.name} - {self.current_stock} unités"
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock
    
    @property
    def is_out_of_stock(self):
        return self.current_stock == 0
    
    @property
    def stock_status(self):
        if self.is_out_of_stock:
            return 'Rupture de stock'
        elif self.is_low_stock:
            return 'Stock faible'
        else:
            return 'En stock'