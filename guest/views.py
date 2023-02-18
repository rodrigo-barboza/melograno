from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

from guest.forms import RegisterForm
from .models import User

import json

def login(request):
	return render(request, 'guest/login.html')	


def password(request):
	return render(request, 'guest/password.html')	


def home(request):
	return render(request, 'guest/pages/home.html')	


def signup(request):
	return render(request, 'guest/signup.html')


@require_POST
@csrf_exempt
def register(request):
	data = json.loads(request.body)
	form = RegisterForm(data)

	if form.is_valid():
		user = User(
			role=form.cleaned_data['user_role'], 
			name=form.cleaned_data['name'],
			email=form.cleaned_data['email'],
			password=make_password(
				form.cleaned_data['password']
			),
			establishment_id=None,
			state='active',
		)

		user.save()

		return JsonResponse({
			'message': 'Usuário cadastrado com sucesso!'
		})
	
	errors = dict(form.errors.items())

	return JsonResponse({'errors': errors}, status=406)

