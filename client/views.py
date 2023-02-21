from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'client/index.html')

def home(request):
	return render(request, 'guest/pages/home.html')	

def carrinho(request):
	return render(request, 'client/carrinho.html')	

