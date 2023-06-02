from cgi import print_exception
from django.db import models

# Create your models here.


class Inventory(models.Model):
    title= models.CharField(max_length=30)
    description= models.CharField(max_length=30)
    price= models.IntegerField()
    quantity= models.IntegerField()
    sku= models.CharField(max_length=10)
