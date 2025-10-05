from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
import csv
import io
from decimal import Decimal
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from stock_app.models import StockLevel


@login_required
def product_list(request):
    products = Product.objects.select_related('category').all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Category filter
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, 'products_app/product_list.html', context)


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products_app/product_detail.html', {'product': product})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('products_app:product_list')
    else:
        form = ProductForm()
    
    return render(request, 'products_app/product_form.html', {'form': form, 'title': 'Create Product'})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('products_app:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products_app/product_form.html', {'form': form, 'title': 'Update Product'})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products_app:product_list')
    
    return render(request, 'products_app/product_confirm_delete.html', {'product': product})


@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products_app/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('products_app:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'products_app/category_form.html', {'form': form, 'title': 'Create Category'})


@login_required
def export_products(request):
    """Export products to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'SKU', 'Category', 'Price', 'Cost Price', 'Status', 'Description'])
    
    products = Product.objects.select_related('category').all()
    for product in products:
        writer.writerow([
            product.name,
            product.sku,
            product.category.name,
            product.price,
            product.cost_price,
            'Active' if product.is_active else 'Inactive',
            product.description
        ])
    
    return response


@login_required
def import_products(request):
    """Import products from CSV"""
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            messages.error(request, 'Veuillez sélectionner un fichier CSV')
            return redirect('products_app:import_products')
        
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Le fichier doit être au format CSV')
            return redirect('products_app:import_products')
        
        try:
            # Read the CSV file
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            created_count = 0
            updated_count = 0
            error_count = 0
            errors = []
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    # Get or create category
                    category_name = row.get('Category', '').strip()
                    if not category_name:
                        errors.append(f"Ligne {row_num}: Catégorie manquante")
                        error_count += 1
                        continue
                    
                    category, _ = Category.objects.get_or_create(
                        name=category_name,
                        defaults={'description': ''}
                    )
                    
                    # Check if product exists
                    sku = row.get('SKU', '').strip()
                    if not sku:
                        errors.append(f"Ligne {row_num}: SKU manquante")
                        error_count += 1
                        continue
                    
                    # Prepare product data
                    product_data = {
                        'name': row.get('Name', '').strip(),
                        'description': row.get('Description', '').strip(),
                        'category': category,
                        'price': Decimal(row.get('Price', 0)),
                        'cost_price': Decimal(row.get('Cost_Price', 0)),
                        'is_active': row.get('Status', 'Active').strip().lower() == 'active'
                    }
                    
                    # Get stock data if present
                    stock_actuel = row.get('Stock_Actuel', '').strip()
                    stock_minimum = row.get('Stock_Minimum', '').strip()
                    
                    # Create or update product
                    product, created = Product.objects.update_or_create(
                        sku=sku,
                        defaults=product_data
                    )
                    
                    # Create or update stock level if stock data is provided
                    if stock_actuel or stock_minimum:
                        stock_level, _ = StockLevel.objects.get_or_create(
                            product=product,
                            defaults={
                                'current_stock': int(stock_actuel) if stock_actuel else 0,
                                'minimum_stock': int(stock_minimum) if stock_minimum else 0,
                            }
                        )
                        if not created:
                            if stock_actuel:
                                stock_level.current_stock = int(stock_actuel)
                            if stock_minimum:
                                stock_level.minimum_stock = int(stock_minimum)
                            stock_level.save()
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                        
                except Exception as e:
                    errors.append(f"Ligne {row_num}: {str(e)}")
                    error_count += 1
            
            # Show results
            if created_count > 0:
                messages.success(request, f'{created_count} produit(s) créé(s)')
            if updated_count > 0:
                messages.success(request, f'{updated_count} produit(s) mis à jour')
            if error_count > 0:
                messages.warning(request, f'{error_count} erreur(s) rencontrée(s)')
                for error in errors[:5]:  # Show first 5 errors
                    messages.error(request, error)
            
            return redirect('products_app:product_list')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'importation: {str(e)}')
            return redirect('products_app:import_products')
    
    return render(request, 'products_app/import_products.html')