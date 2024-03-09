from django.db import models

class Address(models.Model):
    country = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    apartment_suite = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, default=None)

    # address = models.OneToOneField(Address, on_delete=models.CASCADE)


    phone = models.CharField(max_length=20, blank = True)

    def __str__(self):
        return self.name
