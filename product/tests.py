

from django.test import TestCase
from product.models import Product

class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            title="Test Product",
            description="<p>Description of Product</p>",
            price=89.99,
            sku="SKU12321",
            quantity=10,
            cost=50.99
        )

        self.assertEqual(product.title, "Test Product")
        self.assertEqual(product.description, "<p>Description of Product</p>")
        self.assertEqual(product.price, 89.99)
        self.assertEqual(product.sku, "SKU12321")
        self.assertEqual(product.quantity, 10)
        self.assertEqual(product.cost, 50.99)
        # Add more assertions as needed

    # Add more test methods to cover different scenarios

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product
from order.models import OrderItem, Order
from customer.models import Customer
from django.utils import timezone
from decimal import Decimal



class ProductInventoryViewTest(TestCase):
    def setUp(self):
        # Create some products
        self.product1 = Product.objects.create(
            title="Product 1",
            description="Description for Product 1",
            price=10.00,
            sku="SKU1",
            quantity=100,
            cost=5.00,
        )
        self.product2 = Product.objects.create(
            title="Product 2",
            description="Description for Product 2",
            price=20.00,
            sku="SKU2",
            quantity=50,
            cost=10.00,
        )
        self.customer1 = Customer.objects.create(name="Customer 1", email="customer1@example.com", phone="1234567890")
        self.customer2 = Customer.objects.create(name="Customer 2", email="customer2@example.com", phone="9876543210")

        # Create some order items to simulate sold quantities
# Create orders for testing
        self.order1 = Order.objects.create(customer=self.customer1, order_date=timezone.now(), total=Decimal('100.00'))
        self.order2 = Order.objects.create(customer=self.customer2, order_date=timezone.now(), total=Decimal('50.00'))

        # Create order items associated with the orders
        OrderItem.objects.create(order=self.order1, product=self.product1, quantity=20)
        OrderItem.objects.create(order=self.order2, product=self.product2, quantity=30)

def test_product_inventory_view(self):
    # Create an API client
    client = APIClient()

    # Get the URL for the product inventory view
    url = reverse('product-list')

    # Make a GET request to the product inventory API endpoint
    response = client.get(url)

    # Check if the response status code is HTTP 200 OK
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Check the response data
    data = response.json()

    # Check the number of products in the response
    self.assertEqual(len(data), 2)  # Directly check the length of 'data'

    # Check product 1 details
    product1_data = data[0]
    self.assertEqual(product1_data['id'], self.product1.id)
    self.assertEqual(product1_data['title'], self.product1.title)
    self.assertEqual(product1_data['description'], self.product1.description)
    self.assertEqual(product1_data['price'], str(self.product1.price))
    self.assertEqual(product1_data['sku'], self.product1.sku)
    self.assertEqual(product1_data['quantity'], self.product1.quantity)
    self.assertEqual(product1_data['cost'], str(self.product1.cost))
    self.assertEqual(product1_data['current_inventory'], 80)  # 100 - 20 = 80

    # Check product 2 details
    product2_data = data[1]
    self.assertEqual(product2_data['id'], self.product2.id)
    self.assertEqual(product2_data['title'], self.product2.title)
    self.assertEqual(product2_data['description'], self.product2.description)
    self.assertEqual(product2_data['price'], str(self.product2.price))
    self.assertEqual(product2_data['sku'], self.product2.sku)
    self.assertEqual(product2_data['quantity'], self.product2.quantity)
    self.assertEqual(product2_data['cost'], str(self.product2.cost))
    self.assertEqual(product2_data['current_inventory'], 20)  # 50 - 30 = 20



# tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product
from order.models import OrderItem
from customer.models import Customer
from decimal import Decimal

class ProductDetailViewTest(TestCase):
    def setUp(self):
        # Create a test product
        self.product = Product.objects.create(
            title="Test Product",
            description="Description for Test Product",
            price=19.99,
            sku="TEST123",
            quantity=25,
            cost=9.99,
        )

        # Create an order associated with the product
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com",
            phone="1234567890",
        )

        self.order1 = Order.objects.create(
            customer=self.customer,  # Replace with a valid customer if needed
            order_date=timezone.now(),
            total=Decimal('100.00')
        )

        self.order2 = Order.objects.create(
            customer=self.customer,  # Replace with a valid customer if needed
            order_date=timezone.now(),
            total=Decimal('100.00')
        )

        # Create order items to simulate sold quantities
        OrderItem.objects.create(order=self.order1, product=self.product, quantity=10)
        OrderItem.objects.create(order=self.order2, product=self.product, quantity=5)

    def test_get_product_detail(self):
        # Create an API client
        client = APIClient()

        # Get the URL for the product detail view, passing the product's ID
        url = reverse('product-detail', args=[self.product.id])

        # Make a GET request to the product detail API endpoint
        response = client.get(url)

        # Check if the response status code is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        data = response.json()

        # Calculate the current inventory based on order item quantities
        sold_quantities = sum(item.quantity for item in OrderItem.objects.filter(product=self.product))
        current_inventory = self.product.quantity - sold_quantities

        # Check product details in the response, including current inventory
        self.assertEqual(data['id'], self.product.id)
        self.assertEqual(data['title'], self.product.title)
        self.assertEqual(data['description'], self.product.description)
        self.assertEqual(data['price'], str(self.product.price))
        self.assertEqual(data['sku'], self.product.sku)
        self.assertEqual(data['quantity'], self.product.quantity)
        self.assertEqual(data['cost'], str(self.product.cost))
        self.assertEqual(int(data['current_inventory']), current_inventory)


from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product

class ProductCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_product(self):
        url = reverse('product-create')
        data = {
            'title': 'New Product',
            'description': 'Description for New Product',
            'price': '19.99',
            'sku': 'NEW123',
            'quantity': 50,
            'cost': '9.99',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the product was created in the database
        self.assertTrue(Product.objects.filter(title=data['title']).exists())






from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product
from decimal import Decimal, ROUND_DOWN  # Import ROUND_DOWN for rounding


class ProductUpdateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(
            title="Original Product",
            description="Original Description",
            price=19.99,
            sku="ORIGINAL123",
            quantity=25,
            cost=9.99,
        )

def test_update_product(self):
    url = reverse('product-update', args=[self.product.id])
    new_data = {
        'title': 'Updated Product',
        'description': 'Updated Description',
        'price': Decimal('29.99'),  # Convert the price to Decimal
        'sku': 'UPDATED123',
        'quantity': 30,
        'cost': Decimal('15.99'),   # Convert the cost to Decimal
    }

    response = self.client.put(url, new_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Check that the product in the database is updated
    updated_product = Product.objects.get(id=self.product.id)
    self.assertEqual(updated_product.title, new_data['title'])
    self.assertEqual(updated_product.description, new_data['description'])
    
    # Round Decimal values to 2 decimal places for comparison
    self.assertEqual(updated_product.price.quantize(Decimal('0.00'), rounding=ROUND_DOWN), new_data['price'])
    self.assertEqual(updated_product.sku, new_data['sku'])
    self.assertEqual(updated_product.quantity, new_data['quantity'])
    
    # Round the 'cost' Decimal value to 2 decimal places for comparison
    self.assertEqual(updated_product.cost.quantize(Decimal('0.00'), rounding=ROUND_DOWN), new_data['cost'])



from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product

class ProductDeleteViewTest(TestCase):
    def setUp(self):
        # Create a test product
        self.product = Product.objects.create(
            title="Test Product",
            description="Description for Test Product",
            price=19.99,
            sku="TEST123",
            quantity=25,
            cost=9.99,
        )

    def test_delete_product(self):
        # Create an API client
        client = APIClient()

        # Get the URL for deleting the product, passing the product's ID
        url = reverse('product-delete', args=[self.product.id])

        # Make a DELETE request to the product delete API endpoint
        response = client.delete(url)

        # Check if the response status code is HTTP 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the product has been deleted from the database
        self.assertFalse(Product.objects.filter(pk=self.product.id).exists())
