from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem, Tag

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Tag)


