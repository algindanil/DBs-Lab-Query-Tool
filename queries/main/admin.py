from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(CategoryPiece)
admin.site.register(Client)
admin.site.register(Material)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(JeweleryPiece)
