from django.contrib import admin
from .models import User, Establishment, Address, Menu, Order, Plate, Cart, CartItem, OrderItem
# Register your models here.
class UserAppAdmin(admin.ModelAdmin):
    pass


class EstablishmentAdmin(admin.ModelAdmin):
    pass

class AddressAdmin(admin.ModelAdmin):
    pass

class MenuAdmin(admin.ModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    pass

class PlateAdmin(admin.ModelAdmin):
    pass

class CartAdmin(admin.ModelAdmin):
    pass

class CartItemAdmin(admin.ModelAdmin):
    pass

class OrderItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAppAdmin)
admin.site.register(Establishment, EstablishmentAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Plate, PlateAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)