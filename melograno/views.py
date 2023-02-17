from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from melograno.forms import RegisterForm
import json

# Create your views here.
def index(request):
	return render(request, 'melograno/index.html')


def login(request):
	return render(request, 'melograno/login.html')	


def password(request):
	return render(request, 'melograno/password.html')	


def home(request):
	return render(request, 'melograno/pages/home.html')	


def signup(request):
	return render(request, 'melograno/signup.html')


@require_POST
@csrf_exempt
def register(request):
	data = json.loads(request.body)
	print(data)
	form = RegisterForm(data)

	if form.is_valid():
		return JsonResponse({'message': 'tudo ok'})
	
	errors = dict(form.errors.items())
	return JsonResponse({'errors': errors }, status=422)


