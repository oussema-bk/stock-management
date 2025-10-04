from django.urls import path
from . import views

app_name = 'stock_app'

urlpatterns = [
    path('', views.stock_dashboard, name='dashboard'),
    path('list/', views.stock_list, name='stock_list'),
    path('movements/', views.stock_movements, name='movements'),
    path('movements/add/', views.add_stock_movement, name='add_movement'),
    path('level/<int:pk>/update/', views.update_stock_level, name='update_stock_level'),
    path('alerts/', views.stock_alerts, name='alerts'),
    path('api/', views.stock_api, name='stock_api'),
    path('export/', views.export_stock, name='export_stock'),
    path('movements/export/', views.export_movements, name='export_movements'),
]
