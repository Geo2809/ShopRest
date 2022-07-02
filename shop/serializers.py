from decimal import Decimal
from rest_framework import serializers
from .models import  Product


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField()
    def get_price_with_tax(self, product):
        return product.unit_price * Decimal(1.1)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'unit_price', 'inventory', 'price_with_tax', 'collection']    

