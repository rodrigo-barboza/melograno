from django.shortcuts import render

def index(request):
	return render(request, 'melograno/index.html')
