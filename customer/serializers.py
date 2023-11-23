from .models import Address, Customer   
from rest_framework import serializers
from django.db.models import Sum


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

# class CustomerSerializer(serializers.ModelSerializer):
#     address = CustomerAddressSerializer(many=True, read_only=True)  # Include items as a nested field

#     class Meta:
#         model = Customer
#         exclude = ['phone']  # Exclude the 'phone' field if it's not present in the data
from rest_framework import serializers
from order.models import Order

class CustomerSerializer(serializers.ModelSerializer):
    total_orders = serializers.SerializerMethodField()
    total_amount_spent = serializers.SerializerMethodField()

    def get_total_orders(self, customer):
        if isinstance(customer, dict) and 'id' in customer:
            customer_id = customer['id']
            try:
                customer = Customer.objects.get(pk=customer_id)
            except Customer.DoesNotExist:
                return 0
        return customer.order_set.count()

    def get_total_amount_spent(self, customer):
        if isinstance(customer, dict) and 'id' in customer:
            customer_id = customer['id']
            try:
                customer = Customer.objects.get(pk=customer_id)
            except Customer.DoesNotExist:
                return 0
        return customer.order_set.aggregate(total_amount=Sum('total'))['total_amount'] or 0

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'total_orders', 'total_amount_spent']
