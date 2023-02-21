from django. urls import path
from . import views

app_name = 'client'

urlpatterns = [
	path('', views.index, name='index'),
	path('home', views.home, name='home'),
	path('carrinho', views.carrinho, name='carrinho'),

]
