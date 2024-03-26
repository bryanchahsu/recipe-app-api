from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Case, When, OuterRef
from django.http import JsonResponse
from .models import Product
from order.models import OrderItem
from .serializers import ProductSerializer
from rest_framework.views import APIView
from django.db.models import Subquery



class ProductInventoryView(APIView):
    def get(self, request, *args, **kwargs):
        # Use aggregation to calculate the total quantity sold for each product
        sold_quantity_subquery = OrderItem.objects.filter(product=OuterRef('pk')).values('product').annotate(
            total_sold_quantity=Sum('quantity')
        ).values('total_sold_quantity')

        # Use F() expressions to subtract the total sold quantity from the product's initial quantity
        products = Product.objects.annotate(
            total_sold_quantity=ExpressionWrapper(
                F('quantity') - Subquery(sold_quantity_subquery),
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
        inventory_data = serializer.data

        return JsonResponse({'products': inventory_data})
    


    

class ProductDetailView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Calculate the current inventory based on order item quantities
        sold_quantities = sum(item.quantity for item in OrderItem.objects.filter(product=instance))
        instance.current_inventory = max(instance.quantity - sold_quantities, 0)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
