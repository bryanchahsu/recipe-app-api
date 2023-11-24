# from rest_framework import serializers
# from .models import Product

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('id', 'title', 'description', 'price', 'sku', 'quantity', 'cost', 'image')

from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    current_inventory = serializers.DecimalField(max_digits=10, decimal_places=0, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
