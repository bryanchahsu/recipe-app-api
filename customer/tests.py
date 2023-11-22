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

class CustomerViewTest(TestCase):

    print('test for customer list page api')


class CustomerDetailTest(TestCase):
    print("test for creating detail page")


class CustomerCreateTest(TestCase):
    print("test for creating a new customer")


class CustomerUpdateTest(TestCase):
    print("test for creating a update existing customer")


class CustomerDeleteTest(TestCase):
    print("delete an existing customer")