from .models import Address, Customer   
from rest_framework import serializers
from django.db.models import Sum


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        # fields = '__all__'
        fields = ['country', 'street', 'apartment_suite', 'city', 'state', 'zip_code']


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
    # address= CustomerAddressSerializer(many=True, read_only=True)

    address = CustomerAddressSerializer()  # Include the address field

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
    

    def _get_customer_id(self, customer):
        if isinstance(customer, int):
            return customer
        elif isinstance(customer, dict) and 'id' in customer:
            return customer['id']
        return None
    
    def create(self, validated_data):
        address_data = validated_data.pop('address')  # Extract address data
        address_serializer = CustomerAddressSerializer(data=address_data)
        if address_serializer.is_valid():
            address = address_serializer.save()  # Save the address instance
        else:
            raise serializers.ValidationError(address_serializer.errors)

        customer = Customer.objects.create(address=address, **validated_data)
        return customer

    class Meta:
        model = Customer
        # fields = ['id', 'name', 'email', 'total_orders', 'total_amount_spent',
        #         #   'address'
        #           ]
        fields = ['id', 'name', 'email', 'total_orders', 'total_amount_spent', 'address', 'phone']  # Include the address field


class CustomerListSerializer(serializers.ModelSerializer):
    total_orders = serializers.SerializerMethodField()
    total_amount_spent = serializers.SerializerMethodField()
    # address= CustomerAddressSerializer(many=True, read_only=True)

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
        # fields = ['id', 'name', 'email', 'total_orders', 'total_amount_spent',
        #         #   'address'
        #           ]
        fields = ['id', 'name', 'email', 'total_orders', 'total_amount_spent']  # Include the address field


        
# serializers.py
        
from rest_framework import serializers
from .models import Customer, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('country', 'street', 'apartment_suite', 'city', 'state', 'zip_code')

class CustomerCreateSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Customer
        fields = ('name', 'email', 'address', 'phone')

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        customer = Customer.objects.create(address=address, **validated_data)
        return customer



    # def create(self, validated_data):
    #     try:
    #         address_data = validated_data.pop('address')
    #         address_serializer = AddressSerializer(data=address_data)
    #         if address_serializer.is_valid():
    #             address = address_serializer.save()
    #             customer = Customer.objects.create(address=address, **validated_data)
    #             return customer
    #         else:
    #             raise serializers.ValidationError(address_serializer.errors)
    #     except Exception as e:
    #         raise serializers.ValidationError(f"Error occurred during customer creation: {e}")
