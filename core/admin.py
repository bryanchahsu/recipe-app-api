from django.contrib import admin

# Register your models here.


from core.models import Inventory, Recipe


admin.site.register(Inventory)
admin.site.register(Recipe)