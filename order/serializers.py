

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

# class OrderItemSerializer(serializers.ModelSerializer):
#     product = ProductSerializer()

#     class Meta:
#         model = OrderItem
#         # fields = '__all__'
#         # fields = ['id', 'order', 'product', 'quantity']
#         fields = ['product', 'quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def get_product(self, obj):
        if isinstance(obj.product, int):
            # If the product is already a primary key, return it directly
            return obj.product
        else:
            # If the product is an object, return its serialized representation
            return ProductSerializer(obj.product).data



class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    tags = TagSerializer(many=True)  # Use the TagSerializer for tags


    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_date', 'fulfillment_status', 'tags', 'total', 'items']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')  # Extract tags data
        items_data = validated_data.pop('items')  # Extract items data
        order = Order.objects.create(**validated_data)

        # Set tags for the order using the set() method
        tags = [Tag.objects.get_or_create(**tag_data)[0] for tag_data in tags_data]
        order.tags.set(tags)

        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order  # Return the created order instance





    
class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()


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
