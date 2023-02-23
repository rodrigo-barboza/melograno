from django.shortcuts import render
from django.contrib import messages
from social_django.models import UserSocialAuth
from guest.models import User, Establishment
import random

def establishment(request, establishment_id):
	context = {}

	context['establishment'] = establishment_id

	return render(request, 'client/pages/establishment.html', context)

def my_orders(request):
	return render(request, 'client/pages/my-orders.html')

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
	context['establishments'] = get_fancy_establishments(context['establishments'])

	return render(request, 'client/pages/category.html', context)

def index(request):
	context = {}

	if is_social_user(request.user):
		if user_already_registered(request):
			context = { 'user': request.user }
		else:
			messages.error(request, 'Usuário não cadastrado')
			return render(request, 'guest/login.html')
	
	context['establishments'] = get_all_establishments()
	
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
