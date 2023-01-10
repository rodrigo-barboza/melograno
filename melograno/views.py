from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'melograno/index.html')

def login(request):
	return render(request, 'melograno/login.html')	

def password(request):
	return render(request, 'melograno/password.html')	
