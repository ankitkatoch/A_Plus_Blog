from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django_email_verification import send_email
from .models import Account, Profile


def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			username = form.cleaned_data.get('username')
			raw_password = request.POST['password1']
			user = get_user_model().objects.create(username=username, password=make_password(raw_password), email=email)
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			user.is_active = False  # Example
			send_email(user)
			login(request, account)
			messages.info(request, ' We have sent a confirmation mail to your e-mail account. You are just one-step away from our registration process.')
			# messages.info(request, 'You are just one-step away from our registration process.')
			return redirect('blog_list')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'accounts/register.html', context)


def logout_view(request):
	logout(request)
	return redirect('home')


def login_view(request):
	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")
		else:
			messages.error(request, 'Invalid credentials')
			return redirect("login")
	else:
		form = AccountAuthenticationForm()

		context['login_form'] = form
		return render(request, 'accounts/login.html', context)


def profile_view(request, pk):
	object1 = Account.objects.filter(id=pk)
	object_list = {
		'object_list1': object1,
	}
	return render(request, 'accounts/profile.html', object_list)


def update_profile(request, pk):
	if request.POST:
		u_form = AccountUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.info(request, 'Your profile has been updated successfully')
			return redirect('home')
		else:
			messages.info(request, 'Invalid credentials')
	else:
		u_form = AccountUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {
		'u_form': u_form,
		'p_form': p_form,
	}

	return render(request, 'accounts/update_profile.html', context)
