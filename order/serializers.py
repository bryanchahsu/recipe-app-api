

# serializers.py
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Include items as a nested field

    class Meta:
        model = Order
        fields = '__all__'


## FOR THE LIST API VIEW
from rest_framework import serializers
from .models import Order
from django.db import models

class OrderListSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_date', 'fulfillment_status', 'tags', 'total', 'total_quantity']

    def get_total_quantity(self, obj):
        return obj.items.aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
