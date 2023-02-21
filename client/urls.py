from django. urls import path
from django.contrib.auth.decorators import user_passes_test

from . import views

app_name = 'client'

def is_client(user):
	return user.is_authenticated and user.role == 'client'

client_required = user_passes_test(is_client, login_url='/guest/login')

urlpatterns = [
	path('', client_required(views.index), name='index'),
]
