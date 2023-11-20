from django.db import models
from customer.models import Customer  # Assuming you have a Customer model
from product.models import Product  # Import the Product model

class Tag(models.Model):
    name = models.CharField(max_length=255)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    fulfillment_status = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)  # Use the Tag model here
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)  # Set the default product ID here
    quantity = models.PositiveIntegerField()

