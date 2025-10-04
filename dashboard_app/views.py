from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import datetime, timedelta
from products_app.models import Product
from stock_app.models import StockLevel, StockMovement
from sales_app.models import Sale, SaleItem, Customer


@login_required
def main_dashboard(request):
    today = timezone.now().date()
    this_month = today.replace(day=1)
    
    # Product statistics
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    
    # Stock statistics
    total_stock_value = 0
    low_stock_count = 0
    out_of_stock_count = 0
    
    for stock in StockLevel.objects.select_related('product'):
        total_stock_value += stock.current_stock * stock.product.price
        if stock.is_out_of_stock:
            out_of_stock_count += 1
        elif stock.is_low_stock:
            low_stock_count += 1
    
    # Sales statistics
    total_sales = Sale.objects.filter(status='COMPLETED').count()
    today_sales = Sale.objects.filter(sale_date__date=today, status='COMPLETED').count()
    
    total_revenue = Sale.objects.filter(status='COMPLETED').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    today_revenue = Sale.objects.filter(
        sale_date__date=today, 
        status='COMPLETED'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Recent activity
    recent_movements = StockMovement.objects.select_related('product', 'created_by')[:5]
    recent_sales = Sale.objects.filter(status='COMPLETED').select_related('customer')[:5]
    
    # Top selling products
    top_products = SaleItem.objects.filter(
        sale__status='COMPLETED'
    ).values('product__name').annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum('line_total')
    ).order_by('-total_sold')[:5]
    
    # Low stock alerts
    low_stock_items = StockLevel.objects.filter(
        current_stock__lte=F('minimum_stock')
    ).select_related('product')[:5]
    
    context = {
        # Product stats
        'total_products': total_products,
        'active_products': active_products,
        
        # Stock stats
        'total_stock_value': total_stock_value,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        
        # Sales stats
        'total_sales': total_sales,
        'today_sales': today_sales,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        
        # Recent activity
        'recent_movements': recent_movements,
        'recent_sales': recent_sales,
        'top_products': top_products,
        'low_stock_items': low_stock_items,
    }
    return render(request, 'dashboard_app/dashboard.html', context)