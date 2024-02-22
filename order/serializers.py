

# serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from customer.serializers import CustomerSerializer
from product.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Include items as a nested field
    customer = CustomerSerializer()  # Include customer information
    # address= CustomerAddressSerializer()
    # product= ProductSerializer()


    class Meta:
        model = Order
        fields = '__all__'


## FOR THE LIST API VIEW
from rest_framework import serializers
from .models import Order
from django.db import models
from customer.serializers import CustomerSerializer  # Import the CustomerSerializer


class OrderListSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()
    customer = CustomerSerializer()  # Use the CustomerSerializer for the customer field

    

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_date', 'fulfillment_status', 'tags', 'total', 'total_quantity']

    def get_total_quantity(self, obj):
        return obj.items.aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
