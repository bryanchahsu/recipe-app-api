"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

        
    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe object."""
    """1. SHOULD THIS TABLE HAVE ITS OWN BY ITSELF FOR ALL PRODUCTS INFORMATION?
        2. SHOULD THIS TABLE'S QTY BE COMBINED WITH PRODUCTION TABLE TO CREATE AN UPDATED QTY??? """
    """"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    """Recipe object."""
    
    #CORRECT BELOW
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    # )

    # fullname= models.CharField(max_length=30, default="some string")
    # address= models.CharField(max_length=30, default="some string")
    # quantity= models.IntegerField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    names= models.CharField(max_length=30, default="some string")
    description= models.CharField(max_length=30, default="some string")
    quantity= models.IntegerField(default=0)


class Customer(models.Model):
    "customer database"
    name = models.CharField(max_length=30)
    "use email to match with other tables"
    email = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    address = models.CharField(max_length= 1000)
    state = models.CharField(max_length= 1000, null= True)
    business_type = models.CharField(max_length= 100, null= True)

class Invoice(models.Model):
    #"order number as index"
    "use email to match with other tables"

    email = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    item = models.CharField(max_length= 10)
    quantity= models.IntegerField(default=0)

    """FOR INVOICE, SHOULD I REPEAT ALL THE CUSTOMER DETAIL INFORMATION? OR HAVE ANOTHER CUSTOMER INFO TABLE"""
    """ FOR THE QUANTITY UPDATE, DO I COMBINE 'INVOICE TABLE'S' SKU AND QUANTITY TO 'PRODUCTION TABLE' """


#################################################################################################
"ignore below for now"    
class Inventory(models.Model):
    fullname= models.CharField(max_length=30, default="some string")
    address= models.CharField(max_length=30, default="some string")
    quantity= models.IntegerField()

# class Inventory(models.Model):
#     """Recipe object."""
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     time_minutes = models.IntegerField()
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     link = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return self.title




