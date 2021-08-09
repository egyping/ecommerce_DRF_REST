from django.contrib import admin
from .models import UserCheckout, UserAddress, Order
# Register your models here.



class UserCheckoutAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email', 'braintree_id']
    list_filter = ['email', 'user']

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'street', 'city', 'state', 'zipcode']
    list_filter = ['user', 'type']

admin.site.register(UserCheckout, UserCheckoutAdmin)

admin.site.register(UserAddress, UserAddressAdmin)

admin.site.register(Order)