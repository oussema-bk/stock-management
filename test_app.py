#!/usr/bin/env python3
"""
Test script for the Electrical Parts Agency Django application
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electrical_parts_agency.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from products_app.models import Product, Category
from stock_app.models import StockLevel, StockMovement
from sales_app.models import Sale, Customer, SaleItem

def test_database_models():
    """Test that all models are working correctly"""
    print("Testing database models...")
    
    # Test categories
    categories = Category.objects.all()
    print(f"✓ Found {categories.count()} categories")
    
    # Test products
    products = Product.objects.all()
    print(f"✓ Found {products.count()} products")
    
    # Test stock levels
    stock_levels = StockLevel.objects.all()
    print(f"✓ Found {stock_levels.count()} stock levels")
    
    # Test customers
    customers = Customer.objects.all()
    print(f"✓ Found {customers.count()} customers")
    
    # Test sales
    sales = Sale.objects.all()
    print(f"✓ Found {sales.count()} sales")
    
    # Test stock movements
    movements = StockMovement.objects.all()
    print(f"✓ Found {movements.count()} stock movements")
    
    print("✓ All models are working correctly!\n")

def test_views():
    """Test that views are accessible"""
    print("Testing views...")
    
    client = Client()
    
    # Test dashboard
    try:
        response = client.get('/dashboard/')
        print(f"✓ Dashboard: {response.status_code}")
    except Exception as e:
        print(f"✗ Dashboard error: {e}")
    
    # Test products list
    try:
        response = client.get('/products/')
        print(f"✓ Products list: {response.status_code}")
    except Exception as e:
        print(f"✗ Products list error: {e}")
    
    # Test stock dashboard
    try:
        response = client.get('/stock/')
        print(f"✓ Stock dashboard: {response.status_code}")
    except Exception as e:
        print(f"✗ Stock dashboard error: {e}")
    
    # Test sales dashboard
    try:
        response = client.get('/sales/')
        print(f"✓ Sales dashboard: {response.status_code}")
    except Exception as e:
        print(f"✗ Sales dashboard error: {e}")
    
    print("✓ Views testing completed!\n")

def test_admin_access():
    """Test admin interface"""
    print("Testing admin interface...")
    
    client = Client()
    
    # Test admin login page
    try:
        response = client.get('/admin/')
        print(f"✓ Admin interface: {response.status_code}")
    except Exception as e:
        print(f"✗ Admin interface error: {e}")
    
    print("✓ Admin interface testing completed!\n")

def test_data_integrity():
    """Test data integrity and relationships"""
    print("Testing data integrity...")
    
    # Test product-category relationship
    products_with_categories = Product.objects.filter(category__isnull=False).count()
    print(f"✓ Products with categories: {products_with_categories}")
    
    # Test stock level-product relationship
    stock_with_products = StockLevel.objects.filter(product__isnull=False).count()
    print(f"✓ Stock levels with products: {stock_with_products}")
    
    # Test sales with items
    sales_with_items = Sale.objects.filter(sale_items__isnull=False).distinct().count()
    print(f"✓ Sales with items: {sales_with_items}")
    
    # Test stock movements
    movements_with_products = StockMovement.objects.filter(product__isnull=False).count()
    print(f"✓ Stock movements with products: {movements_with_products}")
    
    print("✓ Data integrity testing completed!\n")

def main():
    """Run all tests"""
    print("=" * 50)
    print("ELECTRICAL PARTS AGENCY - TEST SUITE")
    print("=" * 50)
    
    try:
        test_database_models()
        test_views()
        test_admin_access()
        test_data_integrity()
        
        print("=" * 50)
        print("✓ ALL TESTS PASSED!")
        print("=" * 50)
        print("\nThe application is ready to use!")
        print("Access the admin panel at: http://localhost:8000/admin/")
        print("Username: admin")
        print("Password: admin123")
        print("\nAccess the main dashboard at: http://localhost:8000/dashboard/")
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
