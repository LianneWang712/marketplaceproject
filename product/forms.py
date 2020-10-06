from django.forms import ModelForm, TextInput, NumberInput
from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'stock', 'image']
        widgets = {
            'price': NumberInput(attrs={'step': 0.01})
        }
