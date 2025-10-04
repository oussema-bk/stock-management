from django.contrib import admin
from .models import Customer, Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ['product', 'quantity', 'unit_price', 'line_total']
    readonly_fields = ['line_total']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['created_at']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'sale_date', 'status', 'total_amount', 'created_by']
    list_filter = ['status', 'sale_date', 'created_by']
    search_fields = ['customer__name', 'notes']
    raw_id_fields = ['customer', 'created_by']
    inlines = [SaleItemInline]
    readonly_fields = ['sale_date', 'total_amount']


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'product', 'quantity', 'unit_price', 'line_total']
    list_filter = ['sale__sale_date']
    search_fields = ['sale__customer__name', 'product__name']
    raw_id_fields = ['sale', 'product']