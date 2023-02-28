from django.shortcuts import render, redirect
from django.contrib import messages
from django.middleware import csrf
from django.http import JsonResponse
from social_django.models import UserSocialAuth
from django.forms.models import model_to_dict
from guest.models import User, Order, Plate, Cart, Establishment, Menu, CartItem, OrderItem
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import random
import json
import os

def establishment(request, establishment_id):
	context = {}

	establishment = Establishment.objects.filter(establishment_id=establishment_id).first()
	context['establishment'] = get_fancy_establishment(establishment)

	plates = get_menu_with_plates(establishment_id)
	plates = fancy_products(plates)
	plates = Paginator(plates, 4)
	page_number = request.GET.get('page')
	context['plates'] = plates.get_page(page_number)
	
	drinks = get_menu_with_drinks(establishment_id)
	drinks = fancy_products(drinks)
	drinks = Paginator(drinks, 4)
	page_number = request.GET.get('page')
	context['drinks'] = drinks.get_page(page_number)

	return render(request, 'client/pages/establishment.html', context)

def fancy_products(products):
	for product in products:
		if 'guest' in product.image.path:
			product.image = os.path.basename(product.image.path)
	return products

def my_orders(request):
	user_id = request.user.user_id
	order_list = Order.objects.filter(user_id=user_id).all().order_by('-send_time')
	for order in order_list:
		allPlates = OrderItem.objects.filter(order_id = order.order_id).all()
		aux = []
		for item in allPlates:
			aux += Plate.objects.filter(plate_id = item.plate_id.plate_id).all()
		order.plates = aux
	#paginação
	paginator = Paginator(order_list, 3) # Mostra 3 pedidos por página
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {'page_obj': page_obj}
	
	return render(request, 'client/pages/my-orders.html', context)

def profile(request):
	user_id = request.user
	context = {'user_info': user_id}
	return render(request, 'client/pages/profile.html', context)

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
		establishment.image = os.path.basename(establishment.image.path)

	return establishments

def get_fancy_establishment(establishment):
	avg_time = ['20min', '30min', '40min', '50min', '60min']

	establishment.avg_time = random.choice(avg_time)
	establishment.name = establishment.name.title()
	establishment.outline = range(5 - establishment.rate)
	establishment.rate = range(establishment.rate)
	establishment.image = os.path.basename(establishment.image.path)

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

	plate_dict = fix_image(plate)

	return JsonResponse({
		'plate': plate_dict
	}, status=200)

def fix_image(plate):
	fancy_plate  = {}
	fancy_plate['plate_id'] = plate.plate_id
	fancy_plate['name'] = plate.name
	fancy_plate['price'] = plate.price
	fancy_plate['description'] = plate.description
	fancy_plate['category'] = plate.category
	fancy_plate['menu_id'] = plate.menu_id.menu_id
	fancy_plate['image'] = os.path.basename(plate.image.path)

	return fancy_plate

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

@csrf_exempt
def add_to_cart(request):
	current_item = json.loads(request.body)
	current_item = current_item['current_plate']

	user_cart = Cart.objects.filter(
		user_id=request.user.user_id
	).first()

	if not user_cart:
		user_cart = Cart.objects.create(user_id=request.user)

	create_cart_item(user_cart, current_item)

	return JsonResponse({
		'message': 'Adicionado ao carrinho com sucesso.'
	}, status=201)


def create_cart_item(user_cart, current_item):
	plate_id = current_item.get('plate_id')
	plate = Plate.objects.filter(plate_id=plate_id).first()

	CartItem.objects.create(
		cart_id=user_cart,
		plate_id=plate,
		quantity=current_item.get('quantity')
	)

def get_cart_count(request):
	user_cart = Cart.objects.filter(
		user_id=request.user.user_id
	).first()

	if not user_cart:
		return JsonResponse({
			'message': 'Carrinho do usuário vazio'
		}, status=204)
	
	cart_items = CartItem.objects.filter(
		cart_id=user_cart.cart_id
	).all()

	return JsonResponse({
		'message': 'success',
		'cart': list(cart_items.values())
	}, status=200)

@csrf_exempt
def get_cart(request):
	user_cart = Cart.objects.filter(
		user_id=request.user.user_id
	).first()

	if not user_cart:
		return JsonResponse({
			'message': 'Carrinho do usuário vazio'
		}, status=204)
	
	cart_items = CartItem.objects.filter(
		cart_id=user_cart.cart_id
	).all()

	plates = get_cart_plates(cart_items)

	return JsonResponse({
		'cart': plates
	}, status=200, safe=False)


def get_cart_plates(cart_items):
	plates = []

	for cart_item in cart_items:
		plate = Plate.objects.filter(
			plate_id=cart_item.plate_id.plate_id
		).first()

		plates.append({
			'plate_id': plate.plate_id,
			'name': plate.name,
			'price': plate.price,
			'description': plate.description,
			'category': plate.category,
			'quantity': cart_item.quantity
		})

	return plates

@csrf_exempt
def clear_cart(request):
	user_cart = Cart.objects.filter(
		user_id=request.user.user_id
	).first()

	user_cart.delete()

	return JsonResponse({
		'message': 'Carrinho esvaziado'
	}, status=200)


@csrf_exempt
def create_order(request):
	user_cart = Cart.objects.filter(
		user_id=request.user.user_id
	).first()

	order_info = json.loads(request.body)

	is_delivery = True if order_info['delivery'] == 'yes' else False
	payment_method = order_info['payment_method']


	cart_items = CartItem.objects.filter(cart_id=user_cart).all()
	
	establishment_id = get_establishment_id(cart_items)
	order_price = get_order_price(cart_items)

	order = Order.objects.create(
		user_id=request.user,
		establishment_id=establishment_id,
		delivery=is_delivery,
		price=order_price,
		send_time=timezone.now(),
		payment_method=payment_method,
	)

	create_order_items(cart_items, order)

	user_cart.delete()

	return JsonResponse({
		'message': 'Pedido realizado com sucesso!'
	}, status=200)


def create_order_items(cart_items, order):
	for item in cart_items:
		OrderItem.objects.create(
			order_id=order,
			plate_id=item.plate_id,
			quantity=item.quantity
		)

def get_establishment_id(cart_items):
	plate = cart_items[0].plate_id
	plate = Plate.objects.filter(plate_id=plate.plate_id).first()
	menu = Menu.objects.filter(menu_id=plate.menu_id.menu_id).first()
	return menu.establishment_id

def get_order_price(cart_items):
	price = 0.00

	for item in cart_items:
		plate = Plate.objects.filter(plate_id=item.plate_id.plate_id).first()
		price += plate.price * item.quantity

	return price

@csrf_exempt
def establishment_filter(request):
	context = {'csrf_token': csrf.get_token(request)}
	filter = request.POST['establishment_filter']
	establishment = get_filtered_establishment(filter)

	if establishment:
		return redirect('client:establishment', establishment.establishment_id)

	return render(request, 'client/pages/not-found.html')


def get_filtered_establishment(filter):
	establishments = Establishment.objects.all()

	for establishment in establishments:
		if str(filter).lower() in establishment.name.lower():
			return establishment
