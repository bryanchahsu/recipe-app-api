
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Custom query parameter for changing page size
    max_page_size = 50  # Maximum page size allowed


from rest_framework import generics
from .models import Order
from .serializers import OrderListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # filterset_fields = {'order_date': ['gte', 'lte']}  # Date range filter
    filterset_fields = {
        'order_date': ['gte', 'lte'],  # Date range filter
        'fulfillment_status': ['exact'],  # Exact match filter
        # 'tags': ['exact', 'in'],  # Exact match and list membership filter
        'tags__name': ['exact', 'in'],  # Allow exact match and list membership filter for tags

    }
    ordering_fields = '__all__'  # Allow sorting by any valid field
    pagination_class = CustomPageNumberPagination  # Set the pagination class
    




from .models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

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
from product.models import Product
from product.serializers import ProductSerializer

class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer

# class OrderCreateView(generics.CreateAPIView):
#     serializer_class = OrderSerializer
#     # permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can create orders
    
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderCreateSerializer


class OrderCreateView(APIView):
    # def post(self, request):
    #     serializer = OrderSerializer(data=request.data)
    #     if serializer.is_valid():
    #         # Automatically assign the customer based on the request user or any other logic
    #         request.data['customer'] = request.user.customer.id  # Assuming you have a user-customer relationship
            
    #         # Create the order without saving it to the database yet
    #         order = serializer.save() sd                                                                      xc

    #         # Get the ID of the created order
    #         order_id = order.id
            
    #         # Ensure order items have the correct order ID
    #         order_items = request.data.get('items', [])
    #         for item_data in order_items:
    #             item_data['order'] = order_id  # Assign the order ID to each order item

    #         # Create a serializer instance for the order with the updated data
    #         serializer_with_items = OrderSerializer(instance=order, data=request.data)

    #         if serializer_with_items.is_valid():
    #             serializer_with_items.save()  # Save the order with the updated order items
    #             return Response(serializer_with_items.data, status=status.HTTP_201_CREATED)
    #         else:
    #             order.delete()  # Rollback the creation of the order
    #             return Response(serializer_with_items.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()