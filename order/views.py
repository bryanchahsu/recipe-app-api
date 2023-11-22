from .models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# class OrderListView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Retrieve all orders from the database
#         orders = Order.objects.all()

#         # Serialize the orders using the OrderSerializer
#         serializer = OrderSerializer(orders, many=True)

#         # Return serialized orders as a JSON response
#         return Response({"orders": serializer.data})


class OrderListView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all orders from the database along with their related OrderItems
        orders = Order.objects.select_related('customer').prefetch_related('items')

        # Serialize the orders using the OrderSerializer
        serializer = OrderSerializer(orders, many=True)

        # Return serialized orders as a JSON response
        return Response({"orders": serializer.data})
    

    # views.py

from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated  # Import the permission class


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can create orders
 

class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()
