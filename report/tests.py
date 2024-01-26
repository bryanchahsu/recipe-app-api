import random
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from order.models import Order, OrderItem  # Import the relevant models
from customer.models import Customer
from product.models import Product
from django.utils import timezone
from decimal import Decimal

class SalesReportTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create a customer
        self.customer = Customer.objects.create(name="Test Customer")

        # Create a product
        self.product = Product.objects.create(
            title="Test Product",
            description="Product description",
            price=10.0,
            sku="SKU123",
            quantity=100,
            cost=5.0,
        )

        # Create orders with order items
        # Generate random order dates within a range
        order_dates = [
            timezone.make_aware(datetime(2023, 11, 1, 12, 0, 0)),  # November 1, 2023, 12:00 PM
            timezone.make_aware(datetime(2023, 11, 2, 12, 0, 0)),  # November 2, 2023, 12:00 PM
            timezone.make_aware(datetime(2023, 11, 3, 12, 0, 0)),  # November 3, 2023, 12:00 PM
        ]

        self.orders = []
        for order_date in order_dates:
            order = Order.objects.create(
                customer=self.customer,
                order_date=order_date,
                fulfillment_status="Shipped" if random.random() < 0.5 else "Delivered",
                total=str(random.randint(100, 500)),
            )
            OrderItem.objects.create(
                order=order,
                product=self.product,
                quantity=random.randint(1, 5),
            )
            self.orders.append(order)

    def test_total_sales(self):
        # Define the start_date and end_date for your test
        start_date = timezone.make_aware(datetime(2023, 11, 1, 0, 0, 0))  # November 1, 2023, 00:00 AM
        end_date = timezone.make_aware(datetime(2023, 11, 3, 23, 59, 59))  # November 3, 2023, 23:59:59 PM

        # Make a GET request to the SalesReport view with the query parameters
        response = self.client.get(
            reverse("sales-report"),
            {"start_date": start_date, "end_date": end_date}
        )

        # Calculate the expected total_sales based on the orders within the date range
        expected_total_sales = sum(
            float(order.total) for order in self.orders if start_date <= order.order_date <= end_date
        )

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data contains the expected total_sales value
        self.assertEqual(response.data["total_sales"], Decimal(expected_total_sales))

        
    def test_missing_start_date(self):
        end_date = timezone.make_aware(datetime(2023, 11, 3, 23, 59, 59))

        response = self.client.get(
            reverse("sales-report"),
            {"end_date": end_date}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_end_date(self):
        start_date = timezone.make_aware(datetime(2023, 11, 1, 0, 0, 0))

        response = self.client.get(
            reverse("sales-report"),
            {"start_date": start_date}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_end_date_before_start_date(self):
        start_date = timezone.make_aware(datetime(2023, 11, 3, 0, 0, 0))
        end_date = timezone.make_aware(datetime(2023, 11, 1, 0, 0, 0))

        response = self.client.get(
            reverse("sales-report"),
            {"start_date": start_date, "end_date": end_date}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_date_format(self):
        start_date = "invalid_date"
        end_date = timezone.make_aware(datetime(2023, 11, 3, 23, 59, 59))

        response = self.client.get(
            reverse("sales-report"),
            {"start_date": start_date, "end_date": end_date}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_orders_in_date_range(self):
        start_date = timezone.make_aware(datetime(2023, 12, 1, 0, 0, 0))
        end_date = timezone.make_aware(datetime(2023, 12, 31, 23, 59, 59))

        response = self.client.get(
            reverse("sales-report"),
            {"start_date": start_date, "end_date": end_date}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_sales"], Decimal("0.00"))

    def test_negative_total_sales(self):
        start_date = timezone.make_aware(datetime(2023, 11, 1, 0, 0, 0))
        end_date = timezone.make_aware(datetime(2023, 11, 15, 23, 59, 59))

        response = self.client.get(
            reverse("sales-report"),
            {"start_date": start_date, "end_date": end_date}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(float(response.data["total_sales"]), 0)  # Check that total_sales is greater than or equal to zero





# # reports/tests.py
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from django.test import TestCase
# from decimal import Decimal
# from datetime import datetime, timezone
# from order.models import Order, OrderItem
# from product.models import Product
# from customer.models import Customer
# from django.utils import timezone


# class SalesBySKUReportTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#         # Create a customer
#         self.customer = Customer.objects.create(name="Test Customer")

#         # Create a product
#         self.product = Product.objects.create(
#             title="Test Product",
#             description="Product description",
#             price=10.0,
#             sku="SKU123",
#             quantity=100,
#             cost=5.0,
#         )

#         # Create orders with order items
#         self.order1 = Order.objects.create(
#             customer=self.customer,
#             order_date=timezone.now().isoformat(),  # Convert to ISO 8601 format
#             fulfillment_status="Shipped",
#             total="200.00",
#         )

#         OrderItem.objects.create(
#             order=self.order1,
#             product=self.product,
#             quantity=2,
#         )

#     def test_sales_by_sku(self):
#         # Define the start_date and end_date for your test
#         start_date = "2023-11-01T00:00:00Z"
#         end_date = "2023-11-03T23:59:59Z"

#         # Make a GET request to the SalesBySKUReport view with the query parameters
#         response = self.client.get(
#             reverse("sales-by-sku-report"),
#             {"start_date": start_date, "end_date": end_date}
#         )

#         # Assert that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Assert that the response data contains the expected sales data for SKUs
#         self.assertEqual(response.data["sales_by_sku"], [
#             {"product__sku": "SKU123", "total_sales": "200.00"},
#             # Add more entries for other SKUs if needed
#         ])


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from decimal import Decimal
from customer.models import Customer
from product.models import Product
from order.models import Order, OrderItem
import json

class SalesBySKUReportTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create a customer
        self.customer = Customer.objects.create(name="Test Customer")

        # Create products
        self.product1 = Product.objects.create(
            title="Product 1",
            description="Product 1 description",
            price=Decimal("10.0"),
            sku="SKU1",
            quantity=100,
            cost=Decimal("5.0"),
        )

        self.product2 = Product.objects.create(
            title="Product 2",
            description="Product 2 description",
            price=Decimal("15.0"),
            sku="SKU2",
            quantity=50,
            cost=Decimal("7.0"),
        )

        # Create orders with order items
        self.order1 = Order.objects.create(
            customer=self.customer,
            fulfillment_status="Shipped",
            total=Decimal("200.00"),
        )

        OrderItem.objects.create(
            order=self.order1,
            product=self.product1,
            quantity=5,
        )

        self.order2 = Order.objects.create(
            customer=self.customer,
            fulfillment_status="Shipped",
            total=Decimal("300.00"),
        )

        OrderItem.objects.create(
            order=self.order2,
            product=self.product1,
            quantity=4,
        )

        OrderItem.objects.create(
            order=self.order2,
            product=self.product2,
            quantity=2,
        )

    def test_sales_by_sku(self):
        # Make a GET request to the SalesBySKUReport view
        response = self.client.get(reverse("sales-by-sku-report"))

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # print('response:::::')
        # print(response.data)
        
        # # Assert that the response data contains the expected sales data for SKUs
        # self.assertEqual(response.data, [
        #     {"product__sku": "SKU1", "total_sales": Decimal("90.00")},
        #     {"product__sku": "SKU2", "total_sales": Decimal("30.00")},
        # ])

        expected_data = [
            {'product__sku': 'SKU1', 'total_sales': '90.00'},
            {'product__sku': 'SKU2', 'total_sales': '30.00'},
        ]


        # expected_data = [
        #     {"product__sku": "SKU1", "total_sales": "90.00"},
        #     {"product__sku": "SKU2", "total_sales": "30.00"},            
        #     # Add more entries for other SKUs if needed
        # ]
        # print('response:::::')
        # print(response.data)
        # print('expected:::::')
        # print(expected_data)


        # You may need to convert the response data to a list of dictionaries

        # self.assertEqual(response.data, expected_data)
        # Parse the response content as JSON
        # Parse the response data as JSON
        response_data = json.loads(response.content)

        # Ensure the response data is a list (explicitly convert if necessary)
        if not isinstance(response_data, list):
            response_data = [response_data]

        # Define the expected response data with rounded total_sales
        expected_data = [
            {"product__sku": "SKU1", "total_sales": Decimal("90.00").quantize(Decimal("0.00"))},
            {"product__sku": "SKU2", "total_sales": Decimal("30.00").quantize(Decimal("0.00"))},
            # Add more entries for other SKUs if needed
        ]

        # Ensure the response data is a list
        self.assertIsInstance(response_data, list)

        # print(response_data[0]["product__sku"])
        print(expected_data[0]["product__sku"])

        # Iterate through each item in the response and expected data
        for response_item, expected_item in zip(response_data, expected_data):
            # Test if product__sku matches
            print(response_item["product__sku"])

            self.assertEqual(response_item["product__sku"], expected_item["product__sku"])
            
            # Test if total_sales matches (rounding to two decimal places)
            self.assertAlmostEqual(
                Decimal(response_item["total_sales"]), expected_item["total_sales"], places=2
            )
            print(response_item["total_sales"])
