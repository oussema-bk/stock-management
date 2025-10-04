#!/usr/bin/env python3
"""
Test script for export functionality
"""

import os
import sys
import django
import requests
from io import StringIO

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electrical_parts_agency.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_export_functionality():
    """Test all export functionality"""
    print("Testing export functionality...")
    
    client = Client()
    
    # Login as admin
    client.force_login(User.objects.get(username='admin'))
    
    # Test product export
    try:
        response = client.get('/products/export/')
        if response.status_code == 200:
            print("✓ Products export: Working")
            print(f"  Content-Type: {response.get('Content-Type')}")
            print(f"  Content-Disposition: {response.get('Content-Disposition')}")
            print(f"  Content length: {len(response.content)} bytes")
        else:
            print(f"✗ Products export: {response.status_code}")
    except Exception as e:
        print(f"✗ Products export error: {e}")
    
    # Test stock export
    try:
        response = client.get('/stock/export/')
        if response.status_code == 200:
            print("✓ Stock export: Working")
            print(f"  Content-Type: {response.get('Content-Type')}")
            print(f"  Content-Disposition: {response.get('Content-Disposition')}")
            print(f"  Content length: {len(response.content)} bytes")
        else:
            print(f"✗ Stock export: {response.status_code}")
    except Exception as e:
        print(f"✗ Stock export error: {e}")
    
    # Test stock movements export
    try:
        response = client.get('/stock/movements/export/')
        if response.status_code == 200:
            print("✓ Stock movements export: Working")
            print(f"  Content-Type: {response.get('Content-Type')}")
            print(f"  Content-Disposition: {response.get('Content-Disposition')}")
            print(f"  Content length: {len(response.content)} bytes")
        else:
            print(f"✗ Stock movements export: {response.status_code}")
    except Exception as e:
        print(f"✗ Stock movements export error: {e}")
    
    # Test sales export
    try:
        response = client.get('/sales/export/')
        if response.status_code == 200:
            print("✓ Sales export: Working")
            print(f"  Content-Type: {response.get('Content-Type')}")
            print(f"  Content-Disposition: {response.get('Content-Disposition')}")
            print(f"  Content length: {len(response.content)} bytes")
        else:
            print(f"✗ Sales export: {response.status_code}")
    except Exception as e:
        print(f"✗ Sales export error: {e}")
    
    # Test customers export
    try:
        response = client.get('/sales/customers/export/')
        if response.status_code == 200:
            print("✓ Customers export: Working")
            print(f"  Content-Type: {response.get('Content-Type')}")
            print(f"  Content-Disposition: {response.get('Content-Disposition')}")
            print(f"  Content length: {len(response.content)} bytes")
        else:
            print(f"✗ Customers export: {response.status_code}")
    except Exception as e:
        print(f"✗ Customers export error: {e}")
    
    print("\nExport functionality testing completed!")

if __name__ == "__main__":
    test_export_functionality()
