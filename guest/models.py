from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES = (
    ('client','Cliente'),
    ('owner','Proprietário'),
)

STATES = (
    ('active','Ativo'),
    ('inactive','Inativo'),
)

CATEGORIES = (
    ('mexican', 'Mexicana'),
    ('healthy', 'Saudável'),
    ('brazilian', 'Brasileira'),
    ('japanese', 'Japonesa'),
    ('italian', 'Italiana'),
)

STATUS = (
    ('delivered', 'Entregue'),
    ('waiting', 'Aguardando'),
    ('canceled', 'Cancelado'),
    ('in_cart', 'No carrinho'),
)

FOOD_TYPES = (
    ('plate', 'Prato'),
    ('drink', 'Bebida'),
)

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    number = models.IntegerField()

class Establishment(models.Model):
    establishment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=100, null=True)
    rate = models.IntegerField(default=0)
    categories = models.CharField(choices=CATEGORIES, max_length=255)
    delivery = models.BooleanField(default=False)
    opens_at = models.TimeField()
    closes_at = models.TimeField()
    image = models.CharField(max_length=100)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    role = models.CharField(choices=ROLES, max_length=15)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    establishment_id = models.ForeignKey(Establishment, on_delete=models.CASCADE, null=True)
    state = models.CharField(choices=STATES, max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.username

    def is_client(self):
        return self.role == 'client'
    
    def is_owner(self):
        return self.role == 'owner'

class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    establishment_id = models.ForeignKey(Establishment, on_delete=models.CASCADE, null=True)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    establishment_id = models.ForeignKey(Establishment, on_delete=models.CASCADE, null=True)
    delivery = models.BooleanField(default=False)
    price = models.FloatField(default=0.0)
    send_time = models.DateTimeField()
    payment_method = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS, max_length=20, default='waiting')


class Plate(models.Model):
    plate_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    description = models.TextField()
    image = models.CharField(max_length=100)
    category = models.CharField(choices=FOOD_TYPES, max_length=20, default='plate')
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    plate_id = models.ForeignKey(Plate, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    plate_id = models.ForeignKey(Plate, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
