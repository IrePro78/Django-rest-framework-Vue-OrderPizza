from django.contrib import admin

from .models import Order, OrderItem, VariantProduct

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(VariantProduct)