from django.contrib import admin

# Register your models here.
from .models import Customer
from .models import Address

# admin.site.register(Customer)
admin.site.register(Address)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')  # Add 'id' to display the ID

# Register the Customer model with the customized admin class
admin.site.register(Customer, CustomerAdmin)