from django.db.models import Sum  # Import the Sum function from django.db.models

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomerSerializer, CustomerListSerializer
from .models import Customer
from rest_framework import generics

# Create your views here.

from django.db.models import Count, Sum

class CustomerListView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all customers from the database
        customers = Customer.objects.all()

        # Create a list to store customer data with total number of orders and amount spent
        customers_data = []

        # Iterate through each customer
        for customer in customers:
            # Get all orders related to the current customer
            orders = customer.order_set.all()  # Assuming you have a related name 'order_set' in your Customer model
            
            # Calculate the total number of orders for the customer
            total_orders = orders.count()

            # Calculate the total amount spent by the customer
            total_amount_spent = orders.aggregate(Sum('total'))['total__sum']
            if total_amount_spent is None:
                total_amount_spent = 0


            # Serialize the customer data
            customer_data = {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'total_orders': total_orders,
                'total_amount_spent': total_amount_spent,
            }

            customers_data.append(customer_data)

        # Serialize the customers data using the CustomerSerializer
        serializer = CustomerListSerializer(customers_data, many=True)

        # Return serialized customer data as a JSON response
        return Response({"customers": serializer.data})
    


from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer
from django.db.models import Sum
from rest_framework import generics

class CustomerDetailView(APIView):
    def get(self, request, customer_id, *args, **kwargs):
        try:
            # Retrieve the customer from the database based on the customer_id
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            # If the customer doesn't exist, return a 404 response
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Get all orders related to the current customer
        orders = customer.order_set.all()

        # Calculate the total number of orders for the customer
        total_orders = orders.count()

        # Calculate the total amount spent by the customer
        total_amount_spent = orders.aggregate(Sum('total'))['total__sum']
        if total_amount_spent is None:
            total_amount_spent = 0

        # Serialize the customer data
        customer_data = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'total_orders': total_orders,
            'total_amount_spent': total_amount_spent,
        }

        # Serialize the customer data using the CustomerSerializer
        serializer = CustomerSerializer(customer_data)

        # Return serialized customer data as a JSON response
        return Response(serializer.data)
    
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer
from django.shortcuts import get_object_or_404

class CustomerUpdateView(APIView):
    def put(self, request, customer_id):
        # Retrieve the customer object by its ID
        customer = get_object_or_404(Customer, pk=customer_id)
        
        # Serialize the customer data based on the request data
        serializer = CustomerSerializer(customer, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.generics import DestroyAPIView
from .models import Customer
from .serializers import CustomerSerializer

class CustomerDeleteView(DestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer