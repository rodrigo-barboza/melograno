from django. urls import path
from django.contrib.auth.decorators import user_passes_test
from client.views import is_social_user

from . import views

app_name = 'client'

def is_client(user):
	if user.is_authenticated:
		if is_social_user(user):
			return True
		return user.role == 'client'

client_required = user_passes_test(is_client, login_url='/guest/login')

urlpatterns = [
	path('', client_required(views.index), name='index'),
	path('establishment/<int:establishment_id>', client_required(views.establishment), name='establishment'),
	path('my-orders', client_required(views.my_orders), name='my_orders'),
	path('profile', client_required(views.profile), name='profile'),
	path('category/<str:category>', client_required(views.category), name='category'),
	path('plate/<int:plate_id>', client_required(views.get_plate), name='get_plate'),
	path('cart/add-item', client_required(views.add_to_cart), name='add_to_cart'),
	path('cart-info', client_required(views.get_cart_count), name='get_cart_count'),
	path('cart-all-info', client_required(views.get_cart), name='get_cart'),
	path('clear-cart', client_required(views.clear_cart), name='clear_cart'),
	path('order/create', client_required(views.create_order), name='create_order'),
	path('filter/establishment', client_required(views.establishment_filter), name='establishment_filter'),
]
