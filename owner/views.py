from django.shortcuts import render, redirect

def index(request):
	return redirect('owner:establishment_products')

def establishment_details(request):
	return render(request, 'owner/establishment-signup.html')

def establishment_products(request):
	return render(request, 'owner/pages/products.html')

def order_history(request):
	return render(request, 'owner/pages/order-history.html')

def orders(request):
	return render(request, 'owner/pages/orders.html')

def establishment_profile(request):
	return render(request, 'owner/pages/establishment-profile.html')

