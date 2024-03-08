from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from django.urls import reverse
from .models import Order
from .serializers import OrderSerializer, OrderListSerializer



class OrderPaginationTestCase(TestCase):

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

        # Create an order with order items
        self.order = Order.objects.create(
            customer=self.customer,
            order_date="2023-11-21T04:10:29Z",
            fulfillment_status="Pending",
            total="500.00",
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=5,  # Specify the quantity of this product in the order
        )

        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=5,  # Specify the quantity of this product in the order
        )

        # Create 30  additional sample orders with order items
        for i in range(2, 30):  
            order_date = datetime(2023, 11, i, 12, 0, 0)
            order = Order.objects.create(
                customer=self.customer,
                order_date=order_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                fulfillment_status="Shipped" if i % 2 == 0 else "Delivered",
                total=f"{i * 100.00}",
            )
            OrderItem.objects.create(
                order=order,
                product=self.product,
                quantity=i,  # Specify the quantity of this product in the order
            )

    def test_default_pagination(self):
        # Test default pagination settings
        response = self.client.get(reverse("order-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that only the first page (default page size) is returned
        self.assertEqual(len(response.data['results']), 10)  # Assuming default page size is 10


    def test_custom_page_size(self):
        # Test custom page size
        response = self.client.get(reverse("order-list"), {"page_size": 5})  # Set a custom page size of 5
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # Check that only 5 results are returned


    def test_pagination_next_page(self):
        # Test navigating to the next page
        response = self.client.get(reverse("order-list"), {"page": 2})  # Request the second page
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the second page is returned
        self.assertEqual(len(response.data['results']), 10)

        next_url = response.data['next']
        if next_url:
            page_number = int(next_url.split('page=')[1]) - 1
        else:
            # If 'next' is None, it means you are on the last page
            page_number = None
        self.assertEqual(page_number, 2)  # Verify the page number
        


#Test for Sort, Filter, etc

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from django.urls import reverse
from .models import Order
from .serializers import OrderSerializer, OrderListSerializer

class OrderAPITestCase(TestCase):

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

        # Create an order with order items
        self.order = Order.objects.create(
            customer=self.customer,
            order_date="2023-11-21T04:10:29Z",
            fulfillment_status="Pending",
            total="500.00",
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=5,  # Specify the quantity of this product in the order
        )

        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=5,  # Specify the quantity of this product in the order
        )

        # Create four additional sample orders with order items
        for i in range(2, 6):  # Create 4 additional orders
            order_date = datetime(2023, 11, i, 12, 0, 0)
            order = Order.objects.create(
                customer=self.customer,
                order_date=order_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                fulfillment_status="Shipped" if i % 2 == 0 else "Delivered",
                total=f"{i * 100.00}",
            )
            OrderItem.objects.create(
                order=order,
                product=self.product,
                quantity=i,  # Specify the quantity of this product in the order
            )

    def test_date_filtering(self):
        # Test filtering orders by date range
        start_date = "2023-11-02"
        end_date = "2023-11-04"
        response = self.client.get(reverse("order-list"), {"order_date__gte": start_date, "order_date__lte": end_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_orders = Order.objects.filter(order_date__gte=start_date, order_date__lte=end_date)
        serializer = OrderListSerializer(filtered_orders, many=True)

        # Sort the data lists based on the 'id' key before making the assertion
        sorted_response_data = sorted(response.data['results'], key=lambda x: x['id'])
        sorted_serializer_data = sorted(serializer.data, key=lambda x: x['id'])

        # Now, assert that the sorted data lists are equal
        self.assertEqual(sorted_response_data, sorted_serializer_data)

        # self.assertEqual(response.data['results'], serializer.data)

    def test_sorting(self):
        # Test sorting orders by order_date in descending order
        response = self.client.get(reverse("order-list"), {"ordering": "-order_date"})

        #         # Debugging statements
        # print("Response Content:")
        # print(response.content)
        # print("Response Status Code:", response.status_code)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sorted_orders = Order.objects.order_by("-order_date")
        serializer = OrderListSerializer(sorted_orders, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_invalid_date_filtering(self):
        # Test filtering with invalid date format (should return an empty list)
        response = self.client.get(reverse("order-list"), {"order_date__gte": "invalid_date"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_invalid_sorting_field(self):
    #     # Test sorting by an invalid field (should return a bad request status)
    #     response = self.client.get(reverse("order-list"), {"ordering": "invalid_field_name"})
    #     print("reponse:")
    #     print(response.content)
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #NEW TESTS FOR FILTERING AND SORTS

    def test_order_status_filtering(self):
        # Test filtering orders by fulfillment status
        fulfillment_status = "Shipped"
        response = self.client.get(reverse("order-list"), {"fulfillment_status": fulfillment_status})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_orders = Order.objects.filter(fulfillment_status=fulfillment_status)
        serializer = OrderListSerializer(filtered_orders, many=True)
        sorted_response_data = sorted(response.data['results'], key=lambda x: x['id'])
        sorted_serializer_data = sorted(serializer.data, key=lambda x: x['id'])

        # Now, assert that the sorted data lists are equal
        self.assertEqual(sorted_response_data, sorted_serializer_data)


    def test_combined_filtering(self):
        # Test combined filtering by date and fulfillment status
        start_date = "2023-11-02"
        end_date = "2023-11-04"
        fulfillment_status = "Shipped"
        response = self.client.get(reverse("order-list"), {
            "order_date__gte": start_date,
            "order_date__lte": end_date,
            "fulfillment_status": fulfillment_status,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filtered_orders = Order.objects.filter(
            order_date__gte=start_date,
            order_date__lte=end_date,
            fulfillment_status=fulfillment_status,
        )
        serializer = OrderListSerializer(filtered_orders, many=True)
        print(response.data['results'])

        print("serializer data")
        print(serializer.data)

        self.assertEqual(response.data['results'], serializer.data)




# Order List API Test- aggregate on quantity

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Order, OrderItem
from customer.models import Customer
from product.models import Product

class OrderListAPITest(TestCase):
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

        # Create an order with an order item
        self.order = Order.objects.create(
            customer=self.customer,
            order_date="2023-11-21T04:10:29Z",
            fulfillment_status="Pending",
            total="500.00",
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=5,  # Specify the quantity of this product in the order
        )
        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=5,  # Specify the quantity of this product in the order
        )


    def test_order_list_api(self):
        url = reverse('order-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if the JSON response contains the orders and total_quantity
        self.assertEqual(response.data['count'], 1)  # Assuming you have 1 order in the setup
        self.assertEqual(response.data[0]['id'], self.order.id)
        self.assertEqual(response.data[0]['total_quantity'], 10)  # Since you specified a quantity of 5 in the order item
        self.assertEqual(response.data[0]['total'], "500.00")  # Since you specified a quantity of 5 in the order item





## Order Model Testing Only

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
        self.assertEqual(response.data['count'], 1)

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

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class OrderDetailViewTestCase(TestCase):
    def setUp(self):
        # Create a test order and related items
        self.customer = Customer.objects.create(name="Test Customer")
        self.product = Product.objects.create(
            title="Test Product",
            description="Product description",
            price=10.0,
            sku="SKU123",
            quantity=100,
            cost=5.0,
        )
        self.order = Order.objects.create(
            customer=self.customer,
            order_date="2023-11-21T04:10:29Z",
            fulfillment_status="Pending",
            total="500.00",
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=5,  # Specify the quantity of this product in the order
        )
        self.client = APIClient()

    def test_order_detail_view(self):
        # Initialize the API client
        url = reverse('order-detail', args=[self.order.id])  # Generate the URL for the specific order

        # Make a GET request to the order detail view
        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data matches the expected order data
        self.assertEqual(response.data['id'], self.order.id)
        self.assertEqual(response.data['order_date'], self.order.order_date)
        # ... add more assertions for other order fields.

        # Check item information
        self.assertIn('items', response.data)
        self.assertEqual(len(response.data['items']), 1)  # Assuming there is only one item in this order
        self.assertEqual(response.data['items'][0]['product'], self.product.id)
        self.assertEqual(response.data['items'][0]['quantity'], self.order_item.quantity)

    def test_nonexistent_order_detail_view(self):
        # Attempt to fetch the details of a non-existent order
        url = reverse('order-detail', args=[999])  # Use a non-existent ID
        response = self.client.get(url)

        # Check that the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_unauthorized_access(self):
    #     # Create a user without necessary permissions (e.g., using Django's User model)
    #     user = User.objects.create_user(username='testuser', password='testpassword')

    #     # Log in the user using the client (you may need to adjust your authentication settings)
    #     self.client.login(username='testuser', password='testpassword')

    #     # Attempt to access the order detail view
    #     url = reverse('order-detail', args=[self.order.id])
    #     response = self.client.get(url)

    #     # Check that the response status code is 403 (Forbidden) or 401 (Unauthorized) based on your authentication settings
    #     self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])

    def test_post_not_allowed(self):
        # Attempt to make a POST request to the order detail view (should not be allowed)
        url = reverse('order-detail', args=[self.order.id])
        response = self.client.post(url)

        # Check that the response status code is 405 (Method Not Allowed)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_not_allowed(self):
        # Attempt to make a PUT request to the order detail view (should not be allowed)
        url = reverse('order-detail', args=[self.order.id])
        response = self.client.put(url)

        # Check that the response status code is 405 (Method Not Allowed)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)



from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Order, Tag, Customer  # Import your Order model and related models
from .serializers import OrderSerializer  # Import your OrderSerializer

class OrderCreateViewTestCase(TestCase):
    def setUp(self):
        # Create a test user with appropriate permissions using the custom user model
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword', name='Test User')

        # Create a test customer
        self.customer = Customer.objects.create(name='Test Customer')

        # Create a test tag
        self.tag = Tag.objects.create(name='Test Tag')

        # Initialize the API client
        self.client = APIClient()

        # Log in the user using the client
        self.client.force_authenticate(user=self.user)  # Correct way to authenticate the user

        # Define the data for creating an order
        self.order_data = {
            'customer': self.customer.id,  # Use the ID of the created customer
            'order_date': '2023-11-22T04:10:29Z',
            'fulfillment_status': 'Pending',
            'tags': [self.tag.id],  # Use the ID of the created tag in a list
            'total': '500.00',
        }

        #TEST OLD DATA WITHOUT CREATING A TAG OR CUSTOMER 
        # self.order_data = {
        #     'customer': 1,
        #     'order_date': '2023-11-22T04:10:29Z',
        #     'fulfillment_status': 'Pending',
        #     'tags': [1],  # Replace with valid tag IDs,
        #     'total': '500.00',

        # }


    # ... rest of your test methods
    

    def test_create_order(self):
        # Generate the URL for creating a new order
        url = reverse('order-create')

        # Make a POST request to create a new order
        response = self.client.post(url, self.order_data, format='json')


        # Check the response status code (should be 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the order was created in the database (you may need to adjust this based on your model)
        self.assertTrue(Order.objects.filter(order_date='2023-11-22T04:10:29Z').exists())

        # Add more assertions as needed to verify the created order's attributes

    def test_create_order_invalid_data(self):
        # Generate the URL for creating a new order
        url = reverse('order-create')

        # Provide invalid data (e.g., missing required fields)
        invalid_order_data = {
            'order_date': '2023-11-22T04:10:29Z',
        }

        # Make a POST request with invalid data to create a new order
        response = self.client.post(url, invalid_order_data, format='json')

        # Check the response status code (should be 400 Bad Request or another appropriate error status code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Add more test methods for other scenarios and edge cases as needed

    # ...

    

    def test_update_order(self):
        # Create an order to be updated
        order = Order.objects.create(
            customer=self.customer,
            order_date='2023-11-22T04:10:29Z',
            fulfillment_status='Pending',
            total='500.00',
        )

        # Define updated data
        updated_data = {
            'customer': self.customer.id,  # Use the ID of the created customer
            'order_date': '2023-11-23T05:20:30Z',
            'fulfillment_status': 'Shipped',
            'tags': [self.tag.id],  # Use the ID of the created tag in a list
            'total': '600.00',
        }

        # Generate the URL for updating the order
        url = reverse('order-update', args=[order.id])

        # Make a PUT request to update the order
        response = self.client.put(url, updated_data, format='json')

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the order was updated in the database
        updated_order = Order.objects.get(id=order.id)
        expected_datetime = updated_order.order_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.assertEqual(expected_datetime, '2023-11-23T05:20:30Z')

        self.assertEqual(updated_order.fulfillment_status, 'Shipped')
        # Add more assertions as needed to verify other updated attributes

    def test_delete_order(self):
        # Create an order to be deleted
        order = Order.objects.create(
            customer=self.customer,
            order_date='2023-11-22T04:10:29Z',
            fulfillment_status='Pending',
            total='500.00',
        )
        updated_data = {
            'customer': self.customer.id,  # Use the ID of the created customer
            'order_date': '2023-11-23T05:20:30Z',
            'fulfillment_status': 'Shipped',
            'tags': [self.tag.id],  # Use the ID of the created tag in a list
            'total': '600.00',
        }

        # Generate the URL for deleting the order
        url = reverse('order-delete', args=[order.id])

        # Make a DELETE request to delete the order
        # response = self.client.delete(url)
        response = self.client.delete(url, format='json')


        # Check the response status code (should be 204 No Content for successful deletion)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print(response.status_code)

        # Check if the order was deleted from the database
        self.assertFalse(Order.objects.filter(id=order.id).exists())

# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from .models import Customer, Order, OrderItem

# class OrderPostAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.customer = Customer.objects.create(name="Test Customer")
#         self.product1 = Product.objects.create(title="Product 1", price=10.0, cost=5.0)
#         self.product2 = Product.objects.create(title="Product 2", price=15.0, cost=7.5)

#         self.order1 = Order.objects.create(
#             customer=self.customer,
#             order_date="2023-11-19T04:10:29Z",
#             fulfillment_status="Fulfilled",
#             total="9000.00",
#         )
#         self.order2 = Order.objects.create(
#             customer=self.customer,
#             order_date="2023-11-20T04:10:29Z",
#             fulfillment_status="Processing",
#             total="7500.00",
#         )
#         OrderItem.objects.create(order=self.order1, product=self.product1, quantity=2)
#         OrderItem.objects.create(order=self.order2, product=self.product2, quantity=3)
        
#         self.tag1 = Tag.objects.create(name='Tag 1')
#         self.tag2 = Tag.objects.create(name='Tag 2')

#     # def test_create_order(self):
#     #     url = reverse('order-create')
#     #     data = {
#     #         'customer': self.customer.id,
#     #         'order_date': '2024-03-01T12:00:00Z',
#     #         'fulfillment_status': 'Pending',
#     #         'tags': [],
#     #         'total': 50.00,
#     #         'items': [
#     #             {'product': self.product1.id, 'quantity': 2},
#     #             {'product': self.product2.id, 'quantity': 1}
#     #         ]
#     #     }

#     #     response = self.client.post(url, data, format='json')
#     #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     #     self.assertEqual(Order.objects.count(), 3)  # Adjust this based on your expectation
#     #     self.assertEqual(OrderItem.objects.count(), 4)  # Adjust this based on your expectation
        

#     def test_create_order(self):
#         url = reverse('order-create')
        
#         # Create the Address instance
#         address_data = {
#             'country': 'Country',
#             'street': 'Street',
#             'apartment_suite': 'Apartment or Suite',
#             'city': 'City',
#             'state': 'State',
#             'zip_code': 'Zip Code'
#         }
#         address = Address.objects.create(**address_data)

#         data = {
#             'customer': {
#                 'name': 'Test Customer',
#                 'email': 'test@example.com',
#                 'address': address.id  # Pass the ID of the Address instance
#             },
#             'order_date': '2024-03-01T12:00:00Z',
#             'fulfillment_status': 'Pending',
#             'tags': [self.tag1.pk],
#             'total': 50.00,
#             'items': [
#                 {'product': self.product1.pk, 'quantity': 2},
#                 {'product': self.product2.pk, 'quantity': 1}
#             ]
#         }

#         response = self.client.post(url, data, format='json')
#         print(response.content)  # Print out the response content
#         print(response.status_code)  # Print out the response status code

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Order.objects.count(), 1)
#         self.assertEqual(OrderItem.objects.count(), 2)


from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Order
from decimal import Decimal
from .serializers import OrderItemSerializer

class OrderCreateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="Test Customer")
        self.product = Product.objects.create(
            title="Test Product",
            description="Product description",
            price=10.0,
            sku="SKU123",
            quantity=100,
            cost=5.0,
        )

        # Create an order with order items
        self.order = Order.objects.create(
            customer=self.customer,
            order_date="2023-11-21T04:10:29Z",
            fulfillment_status="Pending",
            total="500.00",
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=5,  # Specify the quantity of this product in the order
        )

        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=5,  # Specify the quantity of this product in the order
        )
    def test_products_and_customers_exist(self):
        # Check if products exist
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
        # self.assertTrue(Product.objects.filter(pk=self.product2.pk).exists())

        # Check if customer exists
        self.assertTrue(Customer.objects.filter(pk=self.customer.pk).exists())


    def test_order_serializer(self):
        # Prepare order data
        # order_data = {
        #     'customer': self.customer,
        #     'order_date': '2024-03-01T12:00:00Z',
        #     'fulfillment_status': 'Pending',
        #     'tags': [],
        #     'total': '50.00',
        # }

        customer_instance = Customer.objects.create(name="Test Customer", email="test_customer@example.com")

        order_data_revised = {
            'customer': customer_instance,
            'order_date': '2024-03-01T12:00:00Z',
            'fulfillment_status': 'Pending',
            'tags': [],
            'total': '50.00',
            'items':[
                {'order': 1, 'product': self.product.id, 'quantity': 2},
                # {'order': 1, 'product': self.product.id, 'quantity': 1}
            ]
        }
        # Create order serializer
        order_serializer = OrderSerializer(data=order_data_revised)
        
        if order_serializer.is_valid():
            # Save the order
            order_instance = order_serializer.save()

            # Obtain the ID of the created order
            order_id = order_instance.id

        #     # Prepare order items data with order_id included
        #     order_items_data = [
        #         {'order': order_id, 'product': self.product1.id, 'quantity': 2},
        #         {'order': order_id, 'product': self.product2.id, 'quantity': 1}
        #     ]

        #     # Combine order data and order items data
        #     combined_data = {**order_data, 'items': order_items_data}

        #     # Create order item serializer with combined data
        #     order_item_serializer = OrderSerializer(data=combined_data)
        #     if order_item_serializer.is_valid():
        #         # Save the order with items
        #         order_item_serializer.save()
        #     else:
        #         # Handle order item serializer errors
        #         print(order_item_serializer.errors)
        # else:
        #     # Handle order serializer errors
        #     print(order_serializer.errors)

    # def test_create_order(self):
    #     url = reverse('order-create')
    #     data = {
    #         'customer': self.customer.id,
    #         'order_date': '2024-03-01T12:00:00Z',
    #         'fulfillment_status': 'Pending',
    #         'tags': [],
    #         'total': '50.00',
    #         'items': [
    #             {'product': self.product1.id, 'quantity': 2},
    #             {'product': self.product2.id, 'quantity': 1}
    #         ]
    #     }

    #     response = self.client.post(url, data, format='json')
    #     print(response.content)

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Order.objects.count(), 1)  # Check if an order was created

    #     # Optionally, check the response data to ensure correctness
    #     order_data = response.data
    #     self.assertEqual(order_data['customer'], self.customer.id)
    #     # Check other fields as well...
        