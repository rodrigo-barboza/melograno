from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from social_django.models import UserSocialAuth
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
import random
import json
from guest.models import User, Establishment, Plate, Order, OrderItem, Address, Menu
from django.core.paginator import Paginator

def index(request):
	return redirect('owner:establishment_products2')

def establishment_details(request):
	return render(request, 'owner/establishment-signup.html')

def add_product(request):
	return render(request, 'owner/components/add-product-modal.html')

def establishment_products(request):
	mainEstablishment = request.user.establishment_id
	menus = Menu.objects.filter(establishment_id=mainEstablishment.establishment_id).all()
	aux = []
	for menu in menus:
		aux += Plate.objects.filter(menu_id=menu.menu_id).all()
	#menus.plates = aux
	#page
	paginator = Paginator(aux, 6) # Mostra até 6 pedidos por página
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	context = {'page_obj': page_obj}
	return render(request, 'owner/pages/products.html', context)

def order_history(request):
	mainEstablishment = request.user.establishment_id #daqui tá vindo o estabelecimento já de ctz
	allOrders = Order.objects.filter(establishment_id=mainEstablishment.establishment_id).all()
	for order in allOrders:
		allPlates = OrderItem.objects.filter(order_id = order.order_id).all()
		aux = []
		for item in allPlates:
			aux += Plate.objects.filter(plate_id = item.plate_id.plate_id).all()
		order.plates = aux
	paginator = Paginator(allOrders, 9) # Mostra até 9 pedidos por página
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {'page_obj': page_obj}

	return render(request, 'owner/pages/order-history.html', context)
	#return render(request, 'owner/pages/order-history.html')

def orders(request):
	return render(request, 'owner/pages/orders.html')

def establishment_profile(request):
	mainEstablishment = request.user.establishment_id
	context = {'info':mainEstablishment}
	return render(request, 'owner/pages/establishment-profile.html', context)

