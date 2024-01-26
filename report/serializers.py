from rest_framework import serializers

class SalesBySKUItemSerializer(serializers.Serializer):
    product__sku = serializers.CharField()  # Match the key 'product__sku'
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)  # Match the key 'total_sales'
