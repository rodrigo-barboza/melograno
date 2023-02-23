from django.shortcuts import render
from django.contrib import messages
from social_django.models import UserSocialAuth
from guest.models import User, Order, Plate

def establishment(request):
	return render(request, 'client/pages/establishment.html')

def my_orders(request):
	user_id = request.user.user_id
	order_list = Order.objects.filter(user_id=user_id).all()
	dict = {'order_list': order_list}
	for order in order_list:
		order.plates = Plate.objects.filter(order_id = order.order_id).all()
	return render(request, 'client/pages/my-orders.html', dict)

def profile(request):
	return render(request, 'client/pages/profile.html')

def category(request):
	return render(request, 'client/pages/category.html')

def index(request):
	context = {}

	if is_social_user(request.user):
		if user_already_registered(request):
			context = { 'user': request.user }
		else:
			messages.error(request, 'Usuário não cadastrado')
			return render(request, 'guest/login.html')

	return render(request, 'client/index.html', context)

def is_social_user(request_user):
	has_user = UserSocialAuth.objects.filter(
		user=request_user
	).exists()

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

def register_with_google(request):
	user_query = UserSocialAuth.objects.filter(
		user=request.user
	)

	if user_query.count():
		user_query = user_query.first()
		user = User(
			role='client', 
			name=request.user,
			email=user_query.uid,
			establishment_id=None,
			state='active',
		)

		user.save()
