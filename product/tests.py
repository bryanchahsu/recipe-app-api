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
