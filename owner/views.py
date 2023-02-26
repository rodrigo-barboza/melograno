from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from social_django.models import UserSocialAuth
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
import random
import json
from guest.models import User, Establishment, Plate, Order, OrderItem, Address
from django.core.paginator import Paginator
from .models import Product
from .forms import ProductForm

def index(request):
	return redirect('owner:establishment_products')

def establishment_details(request):
	return render(request, 'owner/establishment-signup.html')

def establishment_products(request):
	products = Product.objects.all()
	return render(request, 'owner/pages/products.html', {'products': products})

def add_product(request):
    if str(request.method) == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            print('hello1')  # adicionado para verificar se os dados estão sendo recebidos corretamente
            form.save()
            return redirect('establishment_products')
        else:
            messages.error(request, 'Please correct the errors below.')
            print('Form is invalid:', form.errors)
    else:
        form = ProductForm()
    return redirect('owner:establishment_products')


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

