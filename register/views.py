from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from .forms import RegisterForm
from .utils import load_cookies_to_user_cart


def register_view(request):
	if request.user.is_authenticated:
		return redirect("home")

	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()

			user = authenticate(
					username = request.POST["username"],
					password = request.POST["password1"]
				)
			if user is not None:
				login(request, user)

			load_cookies_to_user_cart(request)

			return redirect("home")
	else:
		form = RegisterForm()

	context = {
		"form": form,
	}
	return render (request, "register/register.html", context)


def login_view(request):
	if request.user.is_authenticated:
		return redirect("home")

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username = username, password = password)

		if user is not None:
			login(request, user)
			return redirect("/")

		else:
			messages.info(request, "Invalid username or password")
			return redirect("login")

	else:
		return render(request, "register/login.html")


def logout_view(request):
	if request.user.is_authenticated:
		logout(request)
	
	return redirect("home")