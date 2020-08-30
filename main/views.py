from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
# Create your views here.
def homepage(request):
     return render(request = request,
                  template_name='main/home.html',
                  context = {"Posts":Post.objects.all})

# register
def register(request):
     if request.method == "POST":
          form = NewUserForm(request.POST)
          if form.is_valid():
               user = form.save()
               username = form.cleaned_data.get('username')
               messages.success(request, f"New user created: {username}")
               login(request, user)
               messages.info(request, f"Welcome, {username}.")
               return redirect("main:homepage")

          else:
               for msg in form.error_messages:
                    messages.error(request, f"Issue with information provided")

               return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

     form = NewUserForm
     return render(request = request, 
                   template_name = "main/register.html", 
                   context = {"form":form})

# log out 
def logout_request(request):
     logout(request)
     messages.info(request, "You have been logged out.")
     return redirect("main:homepage")

# log in
def login_request(request):
     if request.method == "POST":
          form = AuthenticationForm(request, data=request.POST)
          if form.is_valid():
               username = form.cleaned_data.get('username')
               password = form.cleaned_data.get('password')
               user = authenticate(username=username, password=password)
               if user is not None:
                    login(request, user)
                    messages.info(request, f"Welcome, {username}.")
                    return redirect('/')
               else:
                    messages.error(request, "Invalid username or password.")
          else:
               messages.error(request, "Invalid username or password.")          
     form = AuthenticationForm()               
     return render(request = request,
                   template_name = "main/login.html",
                   context={"form":form})