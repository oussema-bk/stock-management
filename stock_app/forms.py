from django import forms
from .models import StockMovement, StockLevel
from products_app.models import Product


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'reference', 'notes']
        labels = {
            'product': 'Produit',
            'movement_type': 'Type de mouvement',
            'quantity': 'Quantité',
            'reference': 'Référence',
            'notes': 'Notes',
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'movement_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class StockLevelForm(forms.ModelForm):
    class Meta:
        model = StockLevel
        fields = ['minimum_stock', 'maximum_stock']
        labels = {
            'minimum_stock': 'Stock minimum',
            'maximum_stock': 'Stock maximum',
        }
        widgets = {
            'minimum_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'maximum_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
