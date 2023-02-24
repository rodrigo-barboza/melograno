from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from social_django.models import UserSocialAuth
from django.forms.models import model_to_dict
from guest.models import User, Order, Plate, Establishment, Menu
from django.core.paginator import Paginator
import random

def establishment(request, establishment_id):
	context = {}

	establishment = Establishment.objects.filter(establishment_id=establishment_id).first()
	context['establishment'] = get_fancy_establishment(establishment)

	plates = get_menu_with_plates(establishment_id)
	plates = Paginator(plates, 4)
	page_number = request.GET.get('page')
	context['plates'] = plates.get_page(page_number)
	
	drinks = get_menu_with_drinks(establishment_id)
	drinks = Paginator(drinks, 4)
	page_number = request.GET.get('page')
	context['drinks'] = drinks.get_page(page_number)

	return render(request, 'client/pages/establishment.html', context)

def my_orders(request):
	user_id = request.user.user_id
	order_list = Order.objects.filter(user_id=user_id).all()
	for order in order_list:
		order.plates = Plate.objects.filter(order_id = order.order_id).all()
	#paginação
	paginator = Paginator(order_list, 3) # Mostra 3 pedidos por página
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	dict = {'page_obj': page_obj}
	
	return render(request, 'client/pages/my-orders.html', dict)

def profile(request):
	return render(request, 'client/pages/profile.html')

def category(request, category):
	context = {}
	
	categories = {
		'mexican': 'Mexicana',
		'brazilian': 'Brasileira',
    	'healthy': 'Saudável',
    	'japanese': 'Japonesa',
    	'italian': 'Italiana',
	}

	context['category'] = categories[category]
	context['establishments'] = get_establishments_by_category(category)
	context['establishments'] = Paginator(get_fancy_establishments(context['establishments']), 6)
	page_number = request.GET.get('page')
	context['establishments'] = context['establishments'].get_page(page_number)

	return render(request, 'client/pages/category.html', context)

def index(request):
	context = {}

	if is_social_user(request.user):
		if user_already_registered(request):
			context = { 'user': request.user }
		else:
			messages.error(request, 'Usuário não cadastrado')
			return render(request, 'guest/login.html')
	
	context['establishments'] = get_fancy_establishments(get_all_establishments())
	context['establishments'] = Paginator(
		get_fancy_establishments(get_all_establishments()), 9
	)
	page_number = request.GET.get('page')
	context['establishments'] = context['establishments'].get_page(page_number)
	
	return render(request, 'client/index.html', context)

def get_all_establishments():
	return Establishment.objects.all()

def get_establishments_by_category(category):
	return Establishment.objects.filter(categories=category).all()

def get_fancy_establishments(establishments):
	avg_time = ['20min', '30min', '40min', '50min', '60min']

	for establishment in establishments:
		establishment.avg_time = random.choice(avg_time)
		establishment.name = establishment.name.title()
		establishment.outline = range(5 - establishment.rate)
		establishment.rate = range(establishment.rate)

	return establishments

def get_fancy_establishment(establishment):
	avg_time = ['20min', '30min', '40min', '50min', '60min']

	establishment.avg_time = random.choice(avg_time)
	establishment.name = establishment.name.title()
	establishment.outline = range(5 - establishment.rate)
	establishment.rate = range(establishment.rate)

	return establishment

def get_menu_with_plates(establishment_id):
	menu = Menu.objects.filter(
		establishment_id=establishment_id,
	).first()

	return Plate.objects.filter(
		menu_id=menu.menu_id,
		category='plate'
	).all()

def get_menu_with_drinks(establishment_id):
	menu = Menu.objects.filter(
		establishment_id=establishment_id, 
	).first()

	return Plate.objects.filter(
		menu_id=menu.menu_id,
		category='drink'
	).all()

def get_plate(request, plate_id):
	plate = Plate.objects.filter(plate_id=plate_id).first()

	if not plate:
		return JsonResponse({
			'errors': 'Prato não encontrado.'
		}, status=406)

	plate_dict = model_to_dict(plate)

	return JsonResponse({
		'plate': plate_dict
	}, status=200)


def is_social_user(request_user):
	has_user = UserSocialAuth.objects.filter(
		user=request_user
	).exists()

	return True if has_user else False

def user_already_registered(request):
	user_query = UserSocialAuth.objects.filter(
		user=request.user
	)

	if user_query.count():
		user_query = user_query.first()

		has_user = User.objects.filter(
			email=user_query.uid
		).exists()

		return has_user

	return False

def register_with_google(request):
	user_query = UserSocialAuth.objects.filter(
		user=request.user
	)

	if user_query.count():
		user_query = user_query.first()
		user = User(
			role='client', 
			name=request.user,
			email=user_query.uid,
			establishment_id=None,
			state='active',
		)

		user.save()
