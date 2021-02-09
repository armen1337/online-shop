Requirements and some information:


~ Installations

1. python3 -m pip install django-crispy-forms


~ Styles and templates ( register and login )

1. link bootstrap styles in base.html

<link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">


2. <div class="features"> <form class = "form-group"> ...

3. extends 'base.html'


~ Views ( register )

1. Name of view - register_index

2. render ( request, "register/register_index.html", {"form": form'} )

3. form.save(); return redirect( "home" )


~ Forms ( register )

1. Form name - RegisterForm

2. fields = ["username", "email", "password1", "password2"]


~ Settings

1.
CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

2. installed apps - "crispy_forms", "register"

~ Urls

1. path('register/', views.register_index, name="register"),

2. path('', include("django.contrib.auth.urls")), # In the end

