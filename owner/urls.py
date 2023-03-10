from django. urls import path
from django.contrib.auth.decorators import user_passes_test

from . import views

app_name = 'owner'

def is_owner(user):
	return user.is_authenticated and user.role == 'owner'

owner_required = user_passes_test(is_owner, login_url='/guest/login')

urlpatterns = [
	path('', owner_required(views.index), name='index'),
	path('establishment-details', owner_required(views.establishment_details), name='establishment_details'),
	path('add-establishment-info', owner_required(views.set_establishment_info), name='set_establishment_info'),
	path('add-product', owner_required(views.add_product), name='add_product'),
	path('delete-product/<int:plate_id>', owner_required(views.delete_product), name='delete_product'),
	# rotas das páginas
	path('products', owner_required(views.establishment_products), name='establishment_products'),
	path('history', owner_required(views.order_history), name='order_history'),
	path('orders', owner_required(views.orders), name='orders'),
	path('establishment-profile', owner_required(views.establishment_profile), name='establishment_profile'),

]
