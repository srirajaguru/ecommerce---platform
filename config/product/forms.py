from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'product_code',
            'description',
            'size',
            'load_capacity',
            'material',
            'price',
            'image',
            'stock',
            'is_available',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }