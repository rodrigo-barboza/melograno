from django.contrib import admin
from .models import User, Establishment, Address, Menu, Order
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

admin.site.register(User, UserAppAdmin)
admin.site.register(Establishment, EstablishmentAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)