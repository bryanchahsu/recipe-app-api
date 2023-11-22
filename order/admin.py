from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem, Tag

admin.site.register(Order)
admin.site.register(OrderItem)

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Add 'id' to display the ID

# Register the Customer model with the customized admin class
admin.site.register(Tag, TagAdmin)


