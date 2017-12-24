from __future__ import unicode_literals
from .models import User, Compliment
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Sum

def index(request):
	context={
		'users': User.objects.all()
	}
	return render(request, "login_reg/index.html", context)

def registration(request):
	result = User.objects.validate_registration(request.POST)	
	if type(result) == list:
		for err in result:
			messages.error(request, err)
		return redirect('/')
	request.session['user_id'] = result.id
	messages.success(request, "Registration Successful!")
	return redirect('/success')

def login(request):
	result = User.objects.validate_login(request.POST)
	if type(result) == list:
		for err in result:
			messages.error(request, err)
		return redirect('/')
	request.session['user_id'] = result.id
	messages.success(request, "Login Successful!")
	return redirect('/success')

def success(request):
	if 'user_id' not in request.session: #LOOK AT THIS
		return redirect('/')
	current_user = User.objects.get(id = request.session['user_id'])
	context = {
		'current_user': current_user,
		'compliments': Compliment.objects.all(),
		'fav_comps': Compliment.objects.filter(faved_by = current_user).all()
	}	
	# your_favs = Compliment.objects.filter(faved_by = User.objects.get(id = request.session['user_id']))
	return render(request, 'login_reg/success.html', context)

def listofcomps(request):
	try:
		request.session['user_id']
	except Keyerror:
		return redirect('/')

	current_user = User.objects.get(id = request.session['user_id'])
	context = {
		'your_comps': Compliment.objects.filter(author=current_user).all(),
		'compliments': Compliment.objects.all()
	}
	print context['your_comps']
	return render(request, 'login_reg/listofcomps.html', context)

def compliment(request):
	try:
		request.session['user_id']
	except Keyerror:
		return redirect('/')
	print 'hello'
	current_user = User.objects.get(id=request.session['user_id'])
	Compliment.objects.create(
		content = request.POST['content'],
		author = current_user)	

	return redirect('/success')

def favorite(request, comp_id):
	current_user = User.objects.get(id=request.session['user_id'])
	favorite = Compliment.objects.get(id = comp_id).faved_by.add(current_user)

	return redirect('/success')

def logout(request, user_id):
	del request.session
	return redirect('/')
