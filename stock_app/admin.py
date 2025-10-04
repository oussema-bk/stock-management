from django.contrib import admin
from .models import StockMovement, StockLevel


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'reference', 'created_by', 'created_at']
    list_filter = ['movement_type', 'created_at', 'product__category']
    search_fields = ['product__name', 'product__sku', 'reference', 'notes']
    raw_id_fields = ['product', 'created_by']
    readonly_fields = ['created_at']


@admin.register(StockLevel)
class StockLevelAdmin(admin.ModelAdmin):
    list_display = ['product', 'current_stock', 'minimum_stock', 'maximum_stock', 'stock_status', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['product__name', 'product__sku']
    raw_id_fields = ['product']
    readonly_fields = ['last_updated', 'stock_status']