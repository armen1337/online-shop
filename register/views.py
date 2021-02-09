from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm


def register_index(request):
	if request.user.is_authenticated:
		return redirect("home", permanent = True)
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()

			user = authenticate(username = request.POST["username"], password = request.POST["password1"])
			if user is not None:
				login(request, user)

			return redirect("home")
	else:
		form = RegisterForm()

	data = {
		"form": form,
	}
	return render (request, "register/register_index.html", data)