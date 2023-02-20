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


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    number = models.IntegerField()
    lat = models.CharField(max_length=10)
    lng = models.CharField(max_length=10)


class Establishment(models.Model):
    establishment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=100, null=True)
    rate = models.FloatField(default=0.0)
    categories = models.CharField(max_length=255)
    delivery = models.BooleanField(default=False)
    activity_time = models.TimeField()
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
