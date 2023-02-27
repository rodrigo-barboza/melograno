from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

from social_django.models import UserSocialAuth

from melograno.helpers.Mail import Mail

from guest.forms import RegisterForm

from .models import User

import json


def login(request):
	if request.user.is_authenticated:
		if is_social_user(request.user):
			return redirect('client:index')
		return redirect(f'{request.user.role}:index')

	return render(request, 'guest/login.html')

def is_social_user(request_user):
	has_user = UserSocialAuth.objects.filter(
		user=request_user
	).exists()

	return True if has_user else False

def user_logout(request):
	logout(request)
	return redirect('login')

@csrf_exempt
def user_google_login(request):
	if user_already_registered(request):
		user = authenticate_social_user(request)
		auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
		return redirect('client:index')

	messages.error(request, 'Credenciais inválidas')
	return redirect('login')


@csrf_exempt
def user_login(request):
	email = request.POST['email']
	password = request.POST['password']

	user = authenticate(
		request, 
		email=email, 
		password=password
	)

	if user is not None:
		auth_login(request, user)
		return redirect(f'{user.role}:index')

	messages.error(request, 'Email ou senha inválidas')
	return redirect('login')

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

def authenticate_social_user(request):
	user_query = UserSocialAuth.objects.filter(
		user=request.user
	)

	if user_query.count():
		user_query = user_query.first()

		return User.objects.filter(
			email=user_query.uid
		).first()


def redirect_by_role(user):
	if user.role == 'client':
		return 'client:index'

	if user.role == 'owner':
		return 'owner:index'

def password_reset(request):
	return render(request, 'guest/password_reset.html')	

def home(request):
	return render(request, 'guest/pages/home.html')	

def signup(request):
	if request.user.is_authenticated:
		return redirect(f'{request.user.role}:index')
	return render(request, 'guest/signup.html')

def order(request):
	return render(request, 'guest/modalOrder.html')

def products(request):
	return render(request, 'guest/products.html')

def profile(request):
	return render(request, 'guest/profile.html')

@csrf_exempt
def register(request):
	data = json.loads(request.body)
	form = RegisterForm(data)

	if form.is_valid():
		user = User(
			role=form.cleaned_data['user_role'], 
			username=form.cleaned_data['name'],
			email=form.cleaned_data['email'],
			password=make_password(
				form.cleaned_data['password']
			),
			establishment_id=None,
			state='inactive',
		)

		#Mail(
		#	'Confirmação de email',
		#	'Mensagem de teste e tal tal',
		#	user.email
		#).send()

		user.save()

		return JsonResponse({
			'message': 'Usuário cadastrado com sucesso!'
		})

	errors = dict(form.errors.items())

	return JsonResponse({'errors': errors}, status=406)
