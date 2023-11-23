from django.test import TestCase
from customer.models import Customer, Address

class CustomerModelTest(TestCase):
    def test_customer_creation(self):
        # Create an Address instance
        address_data = {
            'country': 'USA',
            'street': '123 Main St',
            'apartment_suite': 'Apt 101',
            'city': 'Anytown',
            'state': 'StateX',
            'zip_code': '12345',
        }
        address = Address.objects.create(**address_data)

        # Create a Customer instance with the associated Address
        customer_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'address': address,  # Assign the Address instance
            'phone': '+1-234-567-8901',
        }
        customer = Customer.objects.create(**customer_data)

        # Perform assertions or additional tests as needed
        self.assertEqual(customer.name, 'John Doe')
        self.assertEqual(customer.email, 'johndoe@example.com')

        # You can also assert the related Address data
        self.assertEqual(customer.address.country, 'USA')
        self.assertEqual(customer.address.street, '123 Main St')

        # Additional assertions and tests for the created customer
        # ...

        # Make sure to test other fields and any custom methods you may have

        # For example, if you have a custom method in your Customer model:
        # self.assertEqual(customer.some_custom_method(), expected_value)

# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from .models import Customer, Address
# from order.models import Order, Tag
# from product.models import Product

# class OLDDCustomerListViewTest(TestCase):
#     def setUp(self):
#         # Create test data
#         self.client = APIClient()
#         self.customer_list_url = reverse('customer-list')  # Use the name of your view's URL
#         self.address = Address.objects.create(
#             country="USA",
#             street="123 Main St",
#             apartment_suite="Apt 101",
#             city="Anytown",
#             state="StateX",
#             zip_code="12345",
#         )
#         self.customers = []
#         self.orders = []

#         for i in range(1, 6):
#             customer = Customer.objects.create(
#                 name=f"Customer {i}",
#                 email=f"customer{i}@example.com",
#                 address=self.address,
#                 phone=f"+1-234-567-890{i}",
#             )
#             self.customers.append(customer)

#             tag = Tag.objects.create(name=f"Tag {i}")

#             product = Product.objects.create(
#                 title=f"Product {i}",
#                 description=f"Description of Product {i}",
#                 price=i * 10.0,
#                 sku=f"SKU{i}",
#                 quantity=10,
#                 cost=i * 5.0,
#             )

#             order = Order.objects.create(
#                 customer=customer,
#                 order_date=f"2023-11-2{i}T04:10:29Z",
#                 fulfillment_status="Pending",
#                 total=i * 100.0,
#             )
#             order.tags.add(tag)
#             order.items.create(product=product, quantity=i)
#             self.orders.append(order)

#     def test_customer_list_view(self):
#         response = self.client.get(self.customer_list_url)
        
#         # Check if the response status code is 200 OK
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Check if the response contains the expected number of customers (5 in this case)
#         self.assertEqual(len(response.data['customers']), 5)



from django.test import TestCase
from decimal import Decimal
from datetime import datetime
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from .models import Customer
from order.models import OrderItem, Product, Order
from django.db.models import Sum
from .serializers import CustomerSerializer  # Import your serializer
from .views import CustomerListView  # Import your view
from django.utils import timezone

class CustomerListViewTest(TestCase):
    def setUp(self):
        # Create some customers
        self.customer1 = Customer.objects.create(name="Customer 1", email="customer1@example.com", phone="1234567890")
        self.customer2 = Customer.objects.create(name="Customer 2", email="customer2@example.com", phone="9876543210")

        # Create products with cost values
        self.product1 = Product.objects.create(cost=Decimal('5.00'), price=Decimal('10.00'))
        self.product2 = Product.objects.create(cost=Decimal('10.00'), price=Decimal('20.00'))

        # Create orders for customers with valid order_date values
        self.order1 = Order.objects.create(customer=self.customer1, order_date=timezone.now().isoformat(), total=Decimal('100.00'))
        self.order2 = Order.objects.create(customer=self.customer1, order_date=timezone.now().isoformat(), total=Decimal('50.00'))
        self.order3 = Order.objects.create(customer=self.customer2, order_date=timezone.now().isoformat(), total=Decimal('75.00'))

        # Create order items with quantities
        self.order_item1 = OrderItem.objects.create(order=self.order1, quantity=5, product=self.product1)
        self.order_item2 = OrderItem.objects.create(order=self.order1, quantity=2, product=self.product2)
        self.order_item3 = OrderItem.objects.create(order=self.order2, quantity=3, product=self.product1)
        self.order_item4 = OrderItem.objects.create(order=self.order3, quantity=4, product=self.product2)

    def test_customer_sums(self):
        # Calculate sums for customer1
        customer1 = Customer.objects.get(name="Customer 1")
        order_items_customer1 = OrderItem.objects.filter(order__customer=customer1)
        quantity_sum_customer1 = order_items_customer1.aggregate(Sum('quantity'))['quantity__sum'] or 0
        price_sum_customer1 = order_items_customer1.aggregate(Sum('order__total'))['order__total__sum'] or Decimal('0.00')

        # Calculate sums for customer2
        customer2 = Customer.objects.get(name="Customer 2")
        order_items_customer2 = OrderItem.objects.filter(order__customer=customer2)
        quantity_sum_customer2 = order_items_customer2.aggregate(Sum('quantity'))['quantity__sum'] or 0
        price_sum_customer2 = order_items_customer2.aggregate(Sum('order__total'))['order__total__sum'] or Decimal('0.00')

        # Assertions
        self.assertEqual(quantity_sum_customer1, 10)  # Expected total quantity for customer1
        self.assertEqual(price_sum_customer1, Decimal('250.00'))  # Expected total price for customer1
        self.assertEqual(quantity_sum_customer2, 4)  # Expected total quantity for customer2
        self.assertEqual(price_sum_customer2, Decimal('75.00'))  # Expected total price for customer2

    def test_customer_api(self):
        # Calculate the expected total quantity and total price for customer1
        expected_total_order_quantity_customer1 = 2
        expected_total_price_customer1 = Decimal('150.00')

        # Calculate the expected total quantity and total price for customer2
        expected_total_order_quantity_customer2 = 1
        expected_total_price_customer2 = Decimal('75.00')

        # Create an API client
        client = APIClient()

        # Make a GET request to the customer list API endpoint
        url = reverse('customer-list')
        response = client.get(url)

        # Check if the response status code is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        data = response.json()
        # print("Response Data:::::", data)
        # print("Response Data:::::", len(data["customers"]))

        
        # Ensure there are two customers in the response
        self.assertEqual(len(data["customers"]), 2)

        # Check customer1's data in the response
        customer1_data = data["customers"][0]
        self.assertEqual(customer1_data['name'], "Customer 1")
        self.assertEqual(customer1_data['total_orders'], expected_total_order_quantity_customer1)
        self.assertEqual(Decimal(customer1_data['total_amount_spent']), expected_total_price_customer1)

        # Check customer2's data in the response
        customer2_data = data["customers"][1]
        self.assertEqual(customer2_data['name'], "Customer 2")
        self.assertEqual(customer2_data['total_orders'], expected_total_order_quantity_customer2)
        self.assertEqual(Decimal(customer2_data['total_amount_spent']), expected_total_price_customer2)


class CustomerDetailViewTest(TestCase):
    def setUp(self):

        # Create some customers
        self.customer1 = Customer.objects.create(name="Customer 1", email="customer1@example.com", phone="1234567890")
        self.customer2 = Customer.objects.create(name="Customer 2", email="customer2@example.com", phone="9876543210")
        self.customer = Customer.objects.create(name="Customer ", email="customer@example.com", phone="1234567890")


        # Create products with cost values
        self.product1 = Product.objects.create(cost=Decimal('5.00'), price=Decimal('10.00'))
        self.product2 = Product.objects.create(cost=Decimal('10.00'), price=Decimal('20.00'))

        # Create orders for customers with valid order_date values
        self.order1 = Order.objects.create(customer=self.customer, order_date=timezone.now().isoformat(), total=Decimal('100.00'))
        self.order2 = Order.objects.create(customer=self.customer1, order_date=timezone.now().isoformat(), total=Decimal('50.00'))
        self.order3 = Order.objects.create(customer=self.customer2, order_date=timezone.now().isoformat(), total=Decimal('75.00'))

        # Create order items with quantities
        self.order_item1 = OrderItem.objects.create(order=self.order1, quantity=5, product=self.product1)
        self.order_item2 = OrderItem.objects.create(order=self.order1, quantity=2, product=self.product2)
        self.order_item3 = OrderItem.objects.create(order=self.order2, quantity=3, product=self.product1)
        self.order_item4 = OrderItem.objects.create(order=self.order3, quantity=4, product=self.product2)




        # Create products with cost values
        self.product1 = Product.objects.create(cost=Decimal('5.00'), price=Decimal('10.00'))
        self.product2 = Product.objects.create(cost=Decimal('10.00'), price=Decimal('20.00'))

        # Create an order for the customer with a valid order_date value
        self.order = Order.objects.create(customer=self.customer, order_date=timezone.now(), total=Decimal('100.00'))

        # Create order items with quantities
        self.order_item1 = OrderItem.objects.create(order=self.order, quantity=5, product=self.product1)
        self.order_item2 = OrderItem.objects.create(order=self.order, quantity=2, product=self.product2)



    def test_customer_detail_api(self):
        # Calculate the expected total quantity and total price for the customer
        expected_total_order = 2
        expected_total_price = Decimal('200')

        # Create an API client
        client = APIClient()

        # Get the URL for the customer detail view, passing the customer_id as a parameter
        url = reverse('customer-detail', args=[self.customer.id])
        
        # Make a GET request to the customer detail API endpoint
        response = client.get(url)

        # Check if the response status code is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        data = response.json()
        # print(data)
        # Check customer data in the response
        self.assertEqual(data['id'], self.customer.id)
        self.assertEqual(data['name'], self.customer.name)
        self.assertEqual(data['email'], self.customer.email)
        self.assertEqual(data['total_orders'], expected_total_order)
        self.assertEqual(Decimal(data['total_amount_spent']), expected_total_price)


from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer
from django.urls import reverse

class CustomerUpdateViewTest(APITestCase):
    def setUp(self):
        # Create a customer
        self.customer = Customer.objects.create(name="Test Customer", email="test@example.com")

    def test_update_customer(self):
        # Get the URL for the customer update view
        url = reverse('customer-update', args=[self.customer.id])

        # Define the new data for the customer
        new_data = {
            'name': 'Updated Name',
            'email': 'updated@example.com',
        }

        # Make a PUT request to the customer update API endpoint with the new data
        response = self.client.put(url, new_data, format='json')

        # Check if the response status code is HTTP 200 OK (indicating successful update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retrieve the customer from the database to check if the data was updated
        updated_customer = Customer.objects.get(id=self.customer.id)

        # Check if the customer's data has been updated correctly
        self.assertEqual(updated_customer.name, new_data['name'])
        self.assertEqual(updated_customer.email, new_data['email'])
        
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer
from django.urls import reverse

class CustomerDeleteViewTest(APITestCase):
    def setUp(self):
        # Create a customer
        self.customer = Customer.objects.create(name="Test Customer", email="test@example.com")

    def test_delete_customer(self):
        # Get the URL for the customer delete view
        url = reverse('customer-delete', args=[self.customer.id])

        # Make a DELETE request to the customer delete API endpoint
        response = self.client.delete(url)

        # Check if the response status code is HTTP 204 No Content (indicating successful deletion)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to retrieve the deleted customer from the database
        with self.assertRaises(Customer.DoesNotExist):
            deleted_customer = Customer.objects.get(id=self.customer.id)
