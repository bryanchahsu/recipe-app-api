
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

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can create orders
 

class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDeleteView(generics.DestroyAPIView):
    queryset = Order.objects.all()