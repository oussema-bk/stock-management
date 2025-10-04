from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
import csv
from .models import Customer, Sale, SaleItem
from .forms import CustomerForm, SaleForm, SaleItemForm
from products_app.models import Product


@login_required
def sales_dashboard(request):
    # Get sales statistics
    today = timezone.now().date()
    this_month = today.replace(day=1)
    
    total_sales = Sale.objects.filter(status='COMPLETED').count()
    today_sales = Sale.objects.filter(sale_date__date=today, status='COMPLETED').count()
    month_sales = Sale.objects.filter(sale_date__date__gte=this_month, status='COMPLETED').count()
    
    # Revenue statistics
    total_revenue = Sale.objects.filter(status='COMPLETED').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    today_revenue = Sale.objects.filter(
        sale_date__date=today, 
        status='COMPLETED'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    month_revenue = Sale.objects.filter(
        sale_date__date__gte=this_month, 
        status='COMPLETED'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Top selling products
    from django.db.models import F
    top_products = SaleItem.objects.filter(
        sale__status='COMPLETED'
    ).values('product__name').annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('unit_price'))
    ).order_by('-total_sold')[:5]
    
    # Recent sales
    recent_sales = Sale.objects.filter(status='COMPLETED').select_related('customer')[:10]
    
    context = {
        'total_sales': total_sales,
        'today_sales': today_sales,
        'month_sales': month_sales,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'month_revenue': month_revenue,
        'top_products': top_products,
        'recent_sales': recent_sales,
    }
    return render(request, 'sales_app/dashboard.html', context)


@login_required
def sales_list(request):
    sales = Sale.objects.select_related('customer', 'created_by').all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        sales = sales.filter(
            Q(customer__name__icontains=search_query) |
            Q(notes__icontains=search_query)
        )
    
    # Status filter
    status_filter = request.GET.get('status')
    if status_filter:
        sales = sales.filter(status=status_filter)
    
    # Date filter
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        sales = sales.filter(sale_date__date__gte=date_from)
    if date_to:
        sales = sales.filter(sale_date__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(sales, 20)
    page_number = request.GET.get('page')
    sales = paginator.get_page(page_number)
    
    context = {
        'sales': sales,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'sales_app/sales_list.html', context)


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    sale_items = sale.sale_items.select_related('product').all()
    
    context = {
        'sale': sale,
        'sale_items': sale_items,
    }
    return render(request, 'sales_app/sale_detail.html', context)


@login_required
def create_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.created_by = request.user
            sale.save()
            messages.success(request, 'Sale created successfully!')
            return redirect('sales_app:sale_detail', pk=sale.pk)
    else:
        form = SaleForm()
    
    return render(request, 'sales_app/sale_form.html', {'form': form, 'title': 'Create Sale'})


@login_required
def add_sale_item(request, sale_pk):
    sale = get_object_or_404(Sale, pk=sale_pk)
    
    if request.method == 'POST':
        form = SaleItemForm(request.POST)
        if form.is_valid():
            sale_item = form.save(commit=False)
            sale_item.sale = sale
            sale_item.save()
            
            # Update sale total
            sale.calculate_total()
            
            messages.success(request, 'Item added to sale!')
            return redirect('sales_app:sale_detail', pk=sale.pk)
    else:
        form = SaleItemForm()
    
    context = {
        'form': form,
        'sale': sale,
        'title': 'Add Item to Sale'
    }
    return render(request, 'sales_app/sale_item_form.html', context)


@login_required
def customer_list(request):
    customers = Customer.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    customers = paginator.get_page(page_number)
    
    context = {
        'customers': customers,
        'search_query': search_query,
    }
    return render(request, 'sales_app/customer_list.html', context)


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('sales_app:customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'sales_app/customer_form.html', {'form': form, 'title': 'Create Customer'})


@login_required
def sales_analytics(request):
    # Sales data for charts
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Daily sales for the last 30 days
    daily_sales = Sale.objects.filter(
        sale_date__date__gte=start_date,
        sale_date__date__lte=end_date,
        status='COMPLETED'
    ).extra(
        select={'day': 'date(sale_date)'}
    ).values('day').annotate(
        total_sales=Count('id'),
        total_revenue=Sum('total_amount')
    ).order_by('day')
    
    # Monthly sales for the last 12 months
    monthly_sales = Sale.objects.filter(
        status='COMPLETED'
    ).extra(
        select={'month': 'strftime("%Y-%m", sale_date)'}
    ).values('month').annotate(
        total_sales=Count('id'),
        total_revenue=Sum('total_amount')
    ).order_by('month')[:12]
    
    context = {
        'daily_sales': list(daily_sales),
        'monthly_sales': list(monthly_sales),
    }
    return render(request, 'sales_app/analytics.html', context)


@login_required
def sales_api(request):
    """API endpoint for sales data"""
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    daily_sales = Sale.objects.filter(
        sale_date__date__gte=start_date,
        sale_date__date__lte=end_date,
        status='COMPLETED'
    ).extra(
        select={'day': 'date(sale_date)'}
    ).values('day').annotate(
        total_sales=Count('id'),
        total_revenue=Sum('total_amount')
    ).order_by('day')
    
    data = {
        'daily_sales': list(daily_sales),
    }
    
    return JsonResponse(data)


@login_required
def export_sales(request):
    """Export sales to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Sale ID', 'Customer', 'Date', 'Status', 'Total Amount', 'Created By'])
    
    sales = Sale.objects.select_related('customer', 'created_by').all()
    for sale in sales:
        writer.writerow([
            sale.id,
            sale.customer.name,
            sale.sale_date.strftime('%Y-%m-%d %H:%M'),
            sale.get_status_display(),
            sale.total_amount,
            sale.created_by.get_full_name() or sale.created_by.username
        ])
    
    return response


@login_required
def export_customers(request):
    """Export customers to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone', 'Address', 'Created Date'])
    
    customers = Customer.objects.all()
    for customer in customers:
        writer.writerow([
            customer.name,
            customer.email or '',
            customer.phone or '',
            customer.address or '',
            customer.created_at.strftime('%Y-%m-%d')
        ])
    
    return response