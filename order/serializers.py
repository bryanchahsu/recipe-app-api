

# serializers.py
from rest_framework import serializers
from .models import Order, OrderItem, Tag
from customer.serializers import CustomerSerializer
from product.serializers import ProductSerializer

from customer.models import Customer
from product.models import Product

class CustomerField(serializers.RelatedField):
    def to_representation(self, value):
        return CustomerSerializer(value).data

    def to_internal_value(self, data):
        if isinstance(data, int):
            # If data is an integer, return it directly
            return data
        try:
            # Try to get the ID attribute from the object
            return data.id
        except AttributeError:
            # If the object does not have an ID attribute, raise an error
            raise serializers.ValidationError("Invalid input. Expected integer or object with 'id' attribute.")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Change here

    class Meta:
        model = OrderItem
        # fields = '__all__'
        fields = ['id', 'order', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    # customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    customer = CustomerSerializer()
    # customer = CustomerField(queryset=Customer.objects.all())

    tags = TagSerializer(many=True)
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        # fields = '__all__'
        fields = ['id', 'customer', 'order_date', 'fulfillment_status', 'tags', 'total', 'items']


    # def create(self, validated_data):
    #     items_data = validated_data.pop('items')
    #     order = Order.objects.create(**validated_data)
    #     for item_data in items_data:
    #         OrderItem.objects.create(order=order, **item_data)
    #     return order        

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        items_data = validated_data.pop('items')
        customer = Customer.objects.create(**customer_data)
        order = Order.objects.create(customer=customer, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

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
