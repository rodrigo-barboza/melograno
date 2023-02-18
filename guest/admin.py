from django.contrib import admin
from .models import User, Establishment, Address
# Register your models here.
class UserAppAdmin(admin.ModelAdmin):
    pass


class EstablishmentAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAppAdmin)
admin.site.register(Establishment, EstablishmentAdmin)
admin.site.register(Address, AddressAdmin)