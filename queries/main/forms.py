from django.forms import ModelForm

from .models import *


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = [
            'name',
            'email',
            'phone_number',
            'address',
        ]


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'client_id',
            'date',
            'status',
        ]


class OrderDetailsForm(ModelForm):
    class Meta:
        model = OrderDetails
        fields = [
            'order_id',
            'piece_id',
            'quantity',
            'price_per_unit',
        ]


class JeweleryPieceForm(ModelForm):
    class Meta:
        model = JeweleryPiece
        fields = [
            'name',
            'price',
            'maker_country',
            'material',
            'categories',
        ]


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
        ]

    
class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = [
            'name',
            'quantity',
            'measurement_unit',
        ]