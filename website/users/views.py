from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm, UserRegistrationForm
from main.views import create_record

# Create your views here.
def custom_login(request):
    #If autherticated, login directly
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    #POST work
    if request.method == "POST":
        form = UserLoginForm(request, request.POST)

        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data["username"], 
                password = form.cleaned_data["password"], 
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b> You have been logged in")
                create_record(request, 'login', 'login')
                return redirect("dashboard")

    else:
        form = UserLoginForm()

    return render(request, "users/login.html", context={"form": form })

@login_required
def custom_logout(request):
    logout(request)
    return redirect('custom_login')

def register(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    #POST working properly
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            create_record(request, 'register', 'register')
            return redirect('dashboard')
        else:
            for error in list(form.errors.values()):
                print(messages(request, error))
            # for key, error in list(form.errors.items()):
            #     if key == 'captcha' and error[0] == 'This field is required.':
            #         messages.error(request, "You may pass the reCAPTICHA test")
            #         continue
            #     messages.error(request, error)
    #If POST is not working, it means that form was not submitted or there is an error
    #submitting the form
    #So in this case, when the form is not submitted, we can simply allow user to 
    #submit the form again
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', context={"form":form})