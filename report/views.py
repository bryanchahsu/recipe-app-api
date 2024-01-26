from decimal import Decimal
from django.db.models import Sum
from datetime import datetime  # Import the datetime class

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from order.models import Order

class SalesReport(APIView):
    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        # Ensure start_date and end_date are provided in the request
        if not start_date or not end_date:
            return Response(
                {"error": "Both start_date and end_date are required query parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Convert start_date and end_date to datetime objects (assuming they are in ISO format)
        try:
            start_date = datetime.fromisoformat(start_date)
            end_date = datetime.fromisoformat(end_date)
        except ValueError:
            return Response(
                {"error": "Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SSZ)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if start_date is after end_date, which is invalid
        if start_date > end_date:
            return Response(
                {"error": "Start date cannot be after end date."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Query the orders within the specified date range
        orders = Order.objects.filter(
            order_date__gte=start_date, order_date__lte=end_date
        )

        # Calculate the total sales within the date range
        total_sales = orders.aggregate(total_sales=Sum("total"))["total_sales"]

        # If there are no orders, set total_sales to 0.00
        if total_sales is None:
            total_sales = Decimal("0.00")

        response_data = {"total_sales": total_sales}
        return Response(response_data, status=status.HTTP_200_OK)


# # reports/views.py
# from decimal import Decimal
# from datetime import datetime
# from django.db.models import Sum
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from order.models import Order, OrderItem

# class SalesBySKUReport(APIView):
#     def get(self, request):
#         start_date = request.query_params.get("start_date")
#         end_date = request.query_params.get("end_date")

#         if not start_date or not end_date:
#             return Response(
#                 {"error": "Both start_date and end_date are required query parameters."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             start_date = datetime.fromisoformat(start_date)
#             end_date = datetime.fromisoformat(end_date)
#         except ValueError:
#             return Response(
#                 {"error": "Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SSZ)."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         if start_date > end_date:
#             return Response(
#                 {"error": "Start date cannot be after end date."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # Query the order items within the specified date range and group by SKU
#         sales_by_sku = OrderItem.objects.filter(
#             order__order_date__gte=start_date,
#             order__order_date__lte=end_date
#         ).values('product__sku').annotate(total_sales=Sum('total'))

#         # If there are no sales, set total_sales to 0.00 for each SKU
#         for entry in sales_by_sku: 
#             if entry['total_sales'] is None:
#                 entry['total_sales'] = Decimal("0.00")

#         response_data = {"sales_by_sku": list(sales_by_sku)}
#         return Response(response_data, status=status.HTTP_200_OK)

# from django.db.models import Sum, F, ExpressionWrapper, DecimalField
# from rest_framework.response import Response
# from order.models import OrderItem
# from .serializers import SalesBySKUItemSerializer
# from rest_framework.views import APIView
# import json

# class SalesBySKUReport(APIView):
#     def get(self, request):
#         # Query to calculate total sales per SKU
#         sales_data = OrderItem.objects.values('product__sku').annotate(
#             total_sales=ExpressionWrapper(
#                 F('quantity') * F('product__price'),
#                 output_field=DecimalField()
#             )
#         )

#         # Convert the data to a list of dictionaries
#         sales_data_list = list(sales_data)

#         # Serialize the data
#         serializer = SalesBySKUItemSerializer(sales_data_list, many=True)

#         # Convert the serialized data to JSON
#         serialized_data = serializer.data
#         json_data = json.dumps(serialized_data)

#         return Response(json_data, content_type='application/json')


from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from rest_framework.response import Response
from order.models import OrderItem
from .serializers import SalesBySKUItemSerializer
from rest_framework.views import APIView
import json

class SalesBySKUReport(APIView):
    def get(self, request):
        # Query to calculate total sales per SKU and aggregate them
        sales_data = OrderItem.objects.values('product__sku').annotate(
            total_sales=Sum(F('quantity') * F('product__price'), output_field=DecimalField())
        )

        # Convert the data to a list of dictionaries
        sales_data_list = list(sales_data)

        # Serialize the data
        serializer = SalesBySKUItemSerializer(sales_data_list, many=True)

        # Convert the serialized data to JSON
        serialized_data = serializer.data
        json_data = json.dumps(serialized_data)

        return Response(json_data, content_type='application/json')
