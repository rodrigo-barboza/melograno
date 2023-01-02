from django. urls import path
from . import views

app_name = 'guest'

urlpatterns = [
	path('', views.index, name='index'),
]
