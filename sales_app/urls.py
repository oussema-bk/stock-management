from django.urls import path
from . import views

app_name = 'sales_app'

urlpatterns = [
    path('', views.sales_dashboard, name='dashboard'),
    path('sales/', views.sales_list, name='sales_list'),
    path('sales/create/', views.create_sale, name='create_sale'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('sales/<int:sale_pk>/add-item/', views.add_sale_item, name='add_sale_item'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('analytics/', views.sales_analytics, name='analytics'),
    path('api/', views.sales_api, name='sales_api'),
    path('export/', views.export_sales, name='export_sales'),
    path('customers/export/', views.export_customers, name='export_customers'),
]
