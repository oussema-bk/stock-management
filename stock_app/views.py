from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, F
from django.http import JsonResponse
from .models import StockMovement, StockLevel
from .forms import StockMovementForm, StockLevelForm
from products_app.models import Product


@login_required
def stock_dashboard(request):
    # Get stock statistics
    total_products = Product.objects.count()
    low_stock_products = StockLevel.objects.filter(current_stock__lte=F('minimum_stock')).count()
    out_of_stock_products = StockLevel.objects.filter(current_stock=0).count()
    
    # Recent movements
    recent_movements = StockMovement.objects.select_related('product', 'created_by')[:10]
    
    # Low stock alerts
    low_stock_items = StockLevel.objects.filter(
        current_stock__lte=F('minimum_stock')
    ).select_related('product')
    
    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'recent_movements': recent_movements,
        'low_stock_items': low_stock_items,
    }
    return render(request, 'stock_app/dashboard.html', context)


@login_required
def stock_list(request):
    stock_levels = StockLevel.objects.select_related('product__category').all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        stock_levels = stock_levels.filter(
            Q(product__name__icontains=search_query) |
            Q(product__sku__icontains=search_query)
        )
    
    # Status filter
    status_filter = request.GET.get('status')
    if status_filter == 'low':
        stock_levels = stock_levels.filter(current_stock__lte=F('minimum_stock'))
    elif status_filter == 'out':
        stock_levels = stock_levels.filter(current_stock=0)
    
    # Pagination
    paginator = Paginator(stock_levels, 20)
    page_number = request.GET.get('page')
    stock_levels = paginator.get_page(page_number)
    
    context = {
        'stock_levels': stock_levels,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'stock_app/stock_list.html', context)


@login_required
def stock_movements(request):
    movements = StockMovement.objects.select_related('product', 'created_by').all()
    
    # Filter by product
    product_filter = request.GET.get('product')
    if product_filter:
        movements = movements.filter(product_id=product_filter)
    
    # Filter by movement type
    type_filter = request.GET.get('type')
    if type_filter:
        movements = movements.filter(movement_type=type_filter)
    
    # Pagination
    paginator = Paginator(movements, 20)
    page_number = request.GET.get('page')
    movements = paginator.get_page(page_number)
    
    products = Product.objects.all()
    
    context = {
        'movements': movements,
        'products': products,
        'product_filter': product_filter,
        'type_filter': type_filter,
    }
    return render(request, 'stock_app/movements.html', context)


@login_required
def add_stock_movement(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.created_by = request.user
            movement.save()
            
            # Update stock level
            stock_level, created = StockLevel.objects.get_or_create(product=movement.product)
            if movement.movement_type == 'IN':
                stock_level.current_stock += movement.quantity
            elif movement.movement_type == 'OUT':
                stock_level.current_stock -= movement.quantity
            elif movement.movement_type == 'ADJUSTMENT':
                stock_level.current_stock = movement.quantity
            
            stock_level.save()
            
            messages.success(request, 'Stock movement recorded successfully!')
            return redirect('stock_app:movements')
    else:
        form = StockMovementForm()
    
    return render(request, 'stock_app/movement_form.html', {'form': form, 'title': 'Add Stock Movement'})


@login_required
def update_stock_level(request, pk):
    stock_level = get_object_or_404(StockLevel, pk=pk)
    if request.method == 'POST':
        form = StockLevelForm(request.POST, instance=stock_level)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock level updated successfully!')
            return redirect('stock_app:stock_list')
    else:
        form = StockLevelForm(instance=stock_level)
    
    return render(request, 'stock_app/stock_level_form.html', {
        'form': form, 
        'title': 'Update Stock Level',
        'stock_level': stock_level
    })


@login_required
def stock_alerts(request):
    low_stock_items = StockLevel.objects.filter(
        current_stock__lte=F('minimum_stock')
    ).select_related('product')
    
    return render(request, 'stock_app/alerts.html', {'low_stock_items': low_stock_items})


@login_required
def stock_api(request):
    """API endpoint for stock data"""
    stock_levels = StockLevel.objects.select_related('product').all()
    data = []
    
    for stock in stock_levels:
        data.append({
            'product_name': stock.product.name,
            'sku': stock.product.sku,
            'current_stock': stock.current_stock,
            'minimum_stock': stock.minimum_stock,
            'status': stock.stock_status,
        })
    
    return JsonResponse(data, safe=False)