from django.contrib import admin
from .models import User, Establishment, Address, Menu, Order, Plate, Cart, CartItem, OrderItem
# Register your models here.
class UserAppAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_login'
    list_display = ('username', 'email', 'role', 'howManyOrders')
    @admin.display(description='Total de pedidos feitos')
    def howManyOrders(self, obj):
        if(obj.role == 'client'):
            order_list = Order.objects.filter(user_id=obj.user_id).all()
            return len(order_list)
        else:
            return 0

class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'categories', 'howManySales')

    @admin.display(description='Total de pedidos vendidos')
    def howManySales(self, obj):
        return len(Order.objects.filter(establishment_id = obj.establishment_id))

class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'district', 'number')

class MenuAdmin(admin.ModelAdmin):
    list_display = ('stablishmentName',)

    @admin.display(description='Estabelecimento referente')
    def stablishmentName(self, obj):
        return Establishment.objects.get(establishment_id = obj.establishment_id.establishment_id).name

class OrderAdmin(admin.ModelAdmin):
    list_display = ('receiver','status','street', 'district', 'value')

    @admin.display(description='Recebedor')
    def receiver(self,obj):
        return obj.user_id 
    
    @admin.display(description='Rua')
    def street(self,obj):
        return obj.address_id.street 
    
    @admin.display(description='Bairro')
    def district(self,obj):
        return obj.address_id.district
    
    @admin.display(description='Valor do Pedido (R$)')
    def value(self,obj):
        return obj.price

class PlateAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'category', 'whereFrom')

    @admin.display(description='Valor do Prato (R$)')
    def value(self,obj):
        return obj.price
    
    @admin.display(description='Estabelecimento referente')
    def whereFrom(self, obj):
        return Establishment.objects.get(establishment_id = obj.menu_id.establishment_id.establishment_id).name
    

class CartAdmin(admin.ModelAdmin):
    pass

class CartItemAdmin(admin.ModelAdmin):
    pass

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('quantity','whatAddressee','whatPlate',)

    @admin.display(description='Recebedor')
    def whatAddressee(self,obj):
        return obj.order_id.user_id

    @admin.display(description='Prato Pedido')
    def whatPlate(self,obj):
        return obj.plate_id.name

admin.site.register(User, UserAppAdmin)
admin.site.register(Establishment, EstablishmentAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Plate, PlateAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)