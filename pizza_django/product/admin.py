from django.contrib import admin

from .models import Category, Product, Topping, Sauce, Size

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Sauce)
admin.site.register(Topping)
admin.site.register(Size)
