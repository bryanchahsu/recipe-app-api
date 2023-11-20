from django.test import TestCase
from order.models import Order
from product.models import Product
from customer.models import Customer, Address  # Import the Address model

class OrderModelTest(TestCase):
  def setUp(self):
    # Create an Address instance
    address_data = {
        "country": "USA",
        "street": "123 Main St",
        "apartment_suite": "Apt 101",
        "city": "Anytown",
        "state": "StateX",
        "zip_code": "12345",
    }
    address = Address.objects.create(**address_data)

    # Create a Customer instance and associate it with the Address
    customer_data = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "address": address,  # Associate the address instance
        "phone": "+1-234-567-8901",
    }
    self.customer = Customer.objects.create(**customer_data)

    # Create Product instances
    self.product1 = Product.objects.create(
        title="Product 1",
        description="Description of Product 1",
        price=89.99,
        sku="SKU12345",
        quantity=10,
        cost=50.99,
    )
    self.product2 = Product.objects.create(
        title="Product 2",
        description="Description of Product 2",
        price=99.99,
        sku="SKU54321",
        quantity=5,
        cost=60.99,
    )

    # Create an Order instance and associate it with the Customer
    order_data = {
        "customer": self.customer.id,  # Use the customer's ID
        "order_date": "2023-07-15T10:00:00Z",
        "fulfillment_status": "Pending",
        "total": 50,
    }
    self.sample_order = Order.objects.create(**order_data)

    # Add Products to the Order with quantities
    self.sample_order.items.create(product=self.product1, quantity=3)
    self.sample_order.items.create(product=self.product2, quantity=2)

def test_order_creation(self):
    # Create an Order instance and associate it with the Customer
    order_data = {
        "customer": self.customer,  # Use the customer object
        "order_date": "2023-07-15T10:00:00Z",
        "fulfillment_status": "Pending",
        "total": 50,
    }
    order = Order.objects.create(**order_data)

    # Add Products to the Order with quantities
    order.items.create(product=self.product1, quantity=3)
    order.items.create(product=self.product2, quantity=2)

    # Assertions
    # Compare with the Customer instance, not a string
    self.assertEqual(order.customer, self.customer)
    self.assertEqual(order.order_date.strftime("%Y-%m-%dT%H:%M:%SZ"), "2023-07-15T10:00:00Z")
    self.assertEqual(order.fulfillment_status, "Pending")
    self.assertEqual(order.total, 50)

    # Check the associated Products and quantities
    self.assertEqual(order.items.count(), 2)
    self.assertEqual(order.items.get(product=self.product1).quantity, 3)
    self.assertEqual(order.items.get(product=self.product2).quantity, 2)


from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Order  # Import your Order model
from customer.models import Customer  # Import the Customer model

class OrderAPITest(TestCase):
    def setUp(self):
        # Create test data
        self.client = APIClient()
        self.order_url = reverse('order-list')  # Use the name of your viewset's URL

        # Create a sample customer
        # Create an Address instance
        address_data = {
            "country": "USA",
            "street": "123 Main St",
            "apartment_suite": "Apt 101",
            "city": "Anytown",
            "state": "StateX",
            "zip_code": "12345",
        }
        address = Address.objects.create(**address_data)

        # Create a Customer instance and associate it with the Address
        customer_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "address": address,  # Provide the address instance
            "phone": "+1-234-567-8901",
        }
        self.customer = Customer.objects.create(**customer_data)



        # Create a sample order associated with the customer
        self.sample_order = Order.objects.create(
            customer=self.customer,
            order_date="2023-07-15T10:00:00Z",
            fulfillment_status="Pending",
            total=50,
        )

    def test_get_all_orders(self):
        response = self.client.get(self.order_url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains the expected number of orders (1 in this case)
        self.assertEqual(len(response.data), 1)

        # You can add more assertions to check the data returned in the response

    # Add more test methods to cover different scenarios
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse  # Import reverse function
from .models import Order, OrderItem
from .serializers import OrderSerializer
from customer.models import Customer  # Import the Customer model
from product.models import Product  # Import the Product model

class OrderListViewTestCase(TestCase):
    def setUp(self):
        # Create test data for orders and items
        customer = Customer.objects.create(name="Test Customer")
        product1 = Product.objects.create(title="Product 1", price=10.0, cost=5.0)
        product2 = Product.objects.create(title="Product 2", price=15.0, cost=7.5)

        order1 = Order.objects.create(
            customer=customer,
            order_date="2023-11-19T04:10:29Z",
            fulfillment_status="Fulfilled",
            total="9000.00",
        )
        order2 = Order.objects.create(
            customer=customer,
            order_date="2023-11-20T04:10:29Z",
            fulfillment_status="Processing",
            total="7500.00",
        )
        OrderItem.objects.create(order=order1, product=product1, quantity=2)
        OrderItem.objects.create(order=order2, product=product2, quantity=3)
def test_order_list_view(self):
    # Initialize the API client
    client = APIClient()
    url = reverse('order-list')  # Use reverse to generate the URL

    # Make a GET request to the order list view
    response = client.get(url)  # Use the generated URL

    # Set maxDiff to None to see the full difference
    self.maxDiff = None

    # Check the response status code
    self.assertEqual(response.status_code, 200)

    # Define the expected data based on the test data you created in setUp
    expected_data = [
        {
            'id': 1,
            'order_date': '2023-11-19T04:10:29Z',
            'fulfillment_status': 'Fulfilled',
            'total': '9000.00',
            'customer': 1,
            'tags': [],
            'items': [{'id': 1, 'product': 1, 'quantity': 2}],
        },
        {
            'id': 2,
            'order_date': '2023-11-20T04:10:29Z',
            'fulfillment_status': 'Processing',
            'total': '7500.00',
            'customer': 1,
            'tags': [],
            'items': [{'id': 2, 'product': 2, 'quantity': 3}],
        },
    ]

    # Check if the response data matches the expected data
    self.assertEqual(response.data, {"orders": expected_data})



