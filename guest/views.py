from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout, login as auth_login
from social_django.models import UserSocialAuth
from django.http import JsonResponse
from social_django.models import UserSocialAuth

from melograno.helpers.Mail import Mail
from guest.forms import RegisterForm
from .models import User

import json

def login(request):
	if request.user.is_authenticated:
		return redirect(f'{request.user.role}:index')

	return render(request, 'guest/login.html')	

def user_logout(request):
	logout(request)
	return redirect('login')

@csrf_exempt
def user_google_login(request):
	if user_already_registered(request):
		user = authenticate_social_user(request)
		auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
		return render(request, 'client/index.html')

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

def password(request):
	return render(request, 'guest/password.html')	

def home(request):
	return render(request, 'guest/pages/home.html')	

def signup(request):
	if request.user.is_authenticated:
		return redirect(f'{request.user.role}:index')
	return render(request, 'guest/signup.html')

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

		Mail(
			'Confirmação de email',
			'Mensagem de teste e tal tal',
			user.email
		).send()

		user.save()

		return JsonResponse({
			'message': 'Usuário cadastrado com sucesso!'
		})

	errors = dict(form.errors.items())

	return JsonResponse({'errors': errors}, status=406)

	user_query = UserSocialAuth.objects.filter(
		user=request.user
	)

	if user_query.count():
		user_query = user_query.first()

		user = User.objects.filter(
			email=user_query.uid
		).first()

		if user:
			messages.error(request, 'Usuário já cadastrado')
			return redirect('signup')

		print('OOOOOOOOOOOOOOOOOOOOO: ',user)
		user = User(
			role='client', 
			username=user_query,
			email=user_query.uid,
			password=None,
			establishment_id=None,
			state='active',
		)

		user.save()

		auth_login(request, user, backend='social_core.backends.google.GoogleOAuth2')

		messages.success(request, 'Usuário cadastrado com sucesso!')
		return redirect('signup')
	else:
		messages.error(request, 'Erro ao cadastrar usuário')
		return redirect('signup')