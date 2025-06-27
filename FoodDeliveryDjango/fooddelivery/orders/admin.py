from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('menu_item', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'restaurant__name', 'delivery_address')
    readonly_fields = ('user', 'restaurant', 'delivery_address', 'contact_phone', 'payment_method', 'total_amount')
    inlines = [OrderItemInline]
    
    def has_add_permission(self, request):
        # Disable ability to add orders through admin (orders should be created through the app)
        return False
