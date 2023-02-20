from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from social_django.models import UserSocialAuth
from social_django.utils import psa
from django.http import HttpResponse
from django.shortcuts import redirect

from melograno.helpers.Mail import Mail
from guest.forms import RegisterForm
from .models import User

import json

def login(request):
	return render(request, 'guest/login.html')

def user_login(request):
	if is_social_user(request.user):
		if user_already_registered(request):
			user = authenticate_social_user(request)
		else:
			messages.error(request, 'Usuário não cadastrado')
			return redirect('login')
	else:
		user = authenticate_user(request)

	if user:
		user_login(request, user.user_id, user.email)
		return redirect_by_role(user)
	
	messages.error(request, 'Credenciais inválidas')
	return redirect('login')

def password(request):
	return render(request, 'guest/password.html')	


def home(request):
	return render(request, 'guest/pages/home.html')	


def signup(request):
	return render(request, 'guest/signup.html')


@csrf_exempt
def register(request):
	if request.method == 'GET':
		return register_with_google(request)

	if request.method == 'POST':
		return register_user(request)


def register_user(request):
	data = json.loads(request.body)
	form = RegisterForm(data)

	if form.is_valid():
		user = User.objects.create_user(

		)
		user = User(
			role=form.cleaned_data['user_role'], 
			name=form.cleaned_data['name'],
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


def register_with_google(request):
	user_query = UserSocialAuth.objects.filter(
		user=request.user
	)

	if user_query.count():
		user_query = user_query.first()

		has_user = User.objects.filter(
			email=user_query.uid
		).exists()

		if has_user:
			messages.error(request, 'Usuário já cadastrado')
			return redirect('signup')

		user = User(
			role='client', 
			name=request.user,
			email=user_query.uid,
			establishment_id=None,
			state='active',
		)

		user.save()

		messages.success(request, 'Usuário cadastrado com sucesso!')
		return redirect('signup')
	else:
		messages.error(request, 'Erro ao cadastrar usuário')
		return redirect('signup')

def get_auth_user(request):
	if bool(len(request.session.items())):
		user = User.objects.filter(
			email=request.session.get('email')
		).first()

		return user
	return None


def redirect_by_role(user):
	if user.role == 'client':
		return redirect('client:index')

	if user.role == 'owner':
		return redirect('owner:index')

def is_social_user(request_user):
	print('fela da puta do caralhooooooooooooooooooo', request_user)
	
	has_user = UserSocialAuth.objects.filter(
		user=request_user
	).exists()

	print(has_user)
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

def authenticate_social_user(request):
	user_query = UserSocialAuth.objects.filter(
		user=request.user
	)

	if user_query.count():
		user_query = user_query.first()

		return User.objects.filter(
			email=user_query.uid
		).first()

def authenticate_user(request):
	data = json.loads(request.body)

	user = User.objects.filter(email=data['email']).first()

	if user:
		user_authenticate(
			email=data['email'],
			password=data['password']
		)

	return user

def user_authenticate(email=None, password=None):
        try:
            user = User.objects.get(username=email)
            if user.check_password(password):
                return user
        except Exception:
            return None

def user_login(request, user_id, email):
	request.session['user_id'] = user_id
	request.session['email'] = email
	request.session.save()


def user_logout(request):
	request.session.clear()


def user_is_authenticated(request):
	has_user = request.session.get('user_id')
	return has_user

def is_client(request):
	user = User.objects.filter(
		email=request.session.get('email')
	).first()

	if user:
		return user.role == 'client'

	return False