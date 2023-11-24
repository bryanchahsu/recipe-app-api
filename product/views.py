from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Case, When, OuterRef
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Product
from order.models import OrderItem
from .serializers import ProductSerializer

class ProductInventoryView(APIView):
    def get(self, request, *args, **kwargs):
        # Use aggregation to calculate the total quantity sold for each product
        sold_quantity = OrderItem.objects.filter(product=OuterRef('pk')).aggregate(
            total_sold_quantity=Sum('quantity')
        )['total_sold_quantity']

        # Use F() expressions to subtract the total sold quantity from the product's initial quantity
        products = Product.objects.annotate(
            total_sold_quantity=ExpressionWrapper(
                F('quantity') - sold_quantity,
                output_field=DecimalField(max_digits=10, decimal_places=0)
            )
        ).annotate(
            current_inventory=Case(
                When(total_sold_quantity__isnull=True, then=F('quantity')),
                default=F('total_sold_quantity'),
                output_field=DecimalField(max_digits=10, decimal_places=0)
            )
        )

        # Serialize the product data using the serializer
        serializer = ProductSerializer(products, many=True)

        # Create a list of dictionaries with product details and inventory levels
        inventory_data = serializer.data

        return JsonResponse({'products': inventory_data})
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from order.models import OrderItem
from django.utils import timezone
from decimal import Decimal
from rest_framework.response import Response

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Calculate the current inventory based on order item quantities
        sold_quantities = sum(item.quantity for item in OrderItem.objects.filter(product=instance))
        instance.current_inventory = max(instance.quantity - sold_quantities, 0)  # Ensure current_inventory is not negative

        serializer = self.get_serializer(instance)
        return Response(serializer.data)



from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



from rest_framework.generics import UpdateAPIView
from .models import Product
from .serializers import ProductSerializer

class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer





from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Product

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  # Replace with your product serializer class
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
