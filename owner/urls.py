from django. urls import path
from django.contrib.auth.decorators import user_passes_test

from . import views

app_name = 'owner'

def is_owner(user):
	return user.is_authenticated and user.role == 'owner'

owner_required = user_passes_test(is_owner, login_url='/guest/login')

urlpatterns = [
	path('', owner_required(views.index), name='index'),
]
