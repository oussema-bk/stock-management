from django import forms
from .models import Customer, Sale, SaleItem
from products_app.models import Product


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']
        labels = {
            'name': 'Nom',
            'email': 'Email',
            'phone': 'Téléphone',
            'address': 'Adresse',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'status', 'notes']
        labels = {
            'customer': 'Client',
            'status': 'Statut',
            'notes': 'Notes',
        }
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'unit_price']
        labels = {
            'product': 'Produit',
            'quantity': 'Quantité',
            'unit_price': 'Prix unitaire',
        }
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_product',
                'onchange': 'updatePrice()'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'id': 'id_unit_price'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show only active products
        products = Product.objects.filter(is_active=True).select_related('stock_level')
        self.fields['product'].queryset = products
        
        # Add help text
        self.fields['product'].help_text = 'Sélectionnez un produit actif'
        self.fields['quantity'].help_text = 'Quantité à vendre'
        self.fields['unit_price'].help_text = 'Prix sera rempli automatiquement'
        
        # Custom label to show stock
        self.fields['product'].label_from_instance = lambda obj: (
            f"{obj.name} ({obj.sku}) - "
            f"Stock: {obj.stock_level.current_stock if hasattr(obj, 'stock_level') else '0'} - "
            f"Prix: ${obj.price}"
        )
