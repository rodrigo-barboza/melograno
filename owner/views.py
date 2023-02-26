from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from social_django.models import UserSocialAuth
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
import json
from guest.models import User, Establishment, Plate, Order, OrderItem, Address
from django.core.paginator import Paginator
from owner.forms import RegisterEstablishmentForm

def index(request):
	if request.user.first_login:
		mark_first_login_as_false(request)
		return redirect('owner:establishment_details')

	return redirect('owner:establishment_products')

def mark_first_login_as_false(request):
	user = User.objects.filter(email=request.user.email).first()
	user.first_login = False
	user.save()

@csrf_exempt
def set_establishment_info(request):
	form = RegisterEstablishmentForm(request.POST, request.FILES)
	
	if form.is_valid():
		delivery = True if request.POST.get('delivery') == 'true' else False

		establishment = Establishment.objects.create(
			name=form.cleaned_data['name'],
			categories=form.cleaned_data['category'],
			delivery=delivery,
			opens_at=form.cleaned_data['opens_at'],			
			closes_at=form.cleaned_data['closes_at'],
			image=form.cleaned_data['name']
		)

		user = User.objects.filter(user_id=request.user.user_id).first()
		user.establishment_id = establishment
		user.save()

		return JsonResponse({
			'message': 'Informações salvas com sucesso!'
		})

	errors = dict(form.errors.items())

	return JsonResponse({'errors': errors}, status=406)


def establishment_details(request):
	return render(request, 'owner/establishment-signup.html')

def add_product(request):
	return render(request, 'owner/components/add-product-modal.html')

def establishment_products(request):
	return render(request, 'owner/pages/products.html')

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

