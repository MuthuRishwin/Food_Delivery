from django.contrib import admin
from .models import UserProfile, Address

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'get_email')
    inlines = [AddressInline]
    search_fields = ('user__username', 'user__email', 'phone_number')
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'address_line1', 'city', 'state', 'postal_code', 'is_default')
    list_filter = ('is_default', 'city', 'state')
    search_fields = ('user_profile__user__username', 'address_line1', 'city', 'state')
