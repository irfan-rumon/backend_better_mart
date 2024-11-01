from django.contrib import admin
from .models import Product, Order, Cart

# Register Product and Order normally
admin.site.register(Product)
admin.site.register(Order)

# Custom admin class for Cart to make it view-only
class CartAdmin(admin.ModelAdmin):
    # Override permissions to disable editing
    def has_change_permission(self, request, obj=None):
        return False  # Prevents editing in the admin

# Register Cart with the custom admin class
admin.site.register(Cart, CartAdmin)
