from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from social_django.models import UserSocialAuth
from guest.models import User
from django.contrib.auth import authenticate, login
import json
from django.http import HttpResponse
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

def index(request):
	if not bool(len(request.session.items())):
		return redirect('login')

	if not is_client(request):
		return redirect('login')

	context = {}
	return render(request, 'client/index.html', context)

def is_client(request):
	user = User.objects.filter(
		email=request.session.get('email')
	).first()

	if user:
		return user.role == 'client'

	return False