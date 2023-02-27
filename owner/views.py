from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from social_django.models import UserSocialAuth
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from guest.models import User, Establishment, Plate, Menu, Order, OrderItem, Address
from django.core.paginator import Paginator
from owner.forms import RegisterEstablishmentForm, PlateForm
import os

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
			image=form.cleaned_data['file']
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

def establishment_products(request):
	mainEstablishment = request.user.establishment_id
	menus = Menu.objects.filter(establishment_id=mainEstablishment.establishment_id).all()
	aux = []
	for menu in menus:
		aux += Plate.objects.filter(menu_id=menu.menu_id).all()
	aux = fancy_plates(aux)

	paginator = Paginator(aux, 6) # Mostra até 6 pedidos por página
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {'page_obj': page_obj}
	return render(request, 'owner/pages/products.html', context)

def fancy_plates(plates):
	categories = {
		'plate': 'Prato',
		'drink': 'Bebida',
	}

	for plate in plates:
		plate.category = categories[plate.category]
		if 'guest' in plate.image.path:
			plate.image = os.path.basename(plate.image.path)

	return plates


@csrf_exempt
def add_product(request):
	form = PlateForm(request.POST, request.FILES)

	establishment_menu = get_establishment_menu(request)

	if form.is_valid():
		Plate.objects.create(
			name=form.cleaned_data['name'],
			price=form.cleaned_data['price'],
			description=form.cleaned_data['description'],
			image=form.cleaned_data['file'],
			category=form.cleaned_data['category'],
			menu_id=establishment_menu,
		)

		return JsonResponse({
			'message': 'Produto adicionado com sucesso!'
		})
	
	errors = dict(form.errors.items())
	return JsonResponse({'errors': errors}, status=406)


def get_establishment_menu(request):
	menu = Menu.objects.filter(
		establishment_id=request.user.establishment_id
	).first()

	if not menu:
		menu = Menu.objects.create(
			establishment_id=request.user.establishment_id
		)

	return menu


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

@csrf_exempt
def delete_product(request, plate_id):
	plate = Plate.objects.filter(
		plate_id=plate_id
	).first()

	if not plate:
		return JsonResponse({
			'message': 'Produto não encontrado'
		}, status=404)

	plate.delete()

	return JsonResponse({
		'message': 'Produto deletado com sucesso!'
	}, status=200)