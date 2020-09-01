import random
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, JsonResponse, Http404
from .models import Post
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm, PostForm
from django.utils.http import is_safe_url

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.

#home page
def homepage(request, *args, **kwargs):
     return render(request,
                  'main/home.html',
                  context = {}, status=200)

# creating posts
def post_create_view(request, *args, **kwargs):
     form = PostForm(request.POST or None) #send data to form
     next_url = request.POST.get("next") or None #getting url from initial page
     if form.is_valid():
          obj = form.save(commit=False)
          obj.save() # save to data base if valid 
          if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
               return redirect(next_url) # redirect to initial page after posting
          form = PostForm()
     return render(request, 'main/includes/form.html', context = {"form": form}) # render form if invalid

# feed
def post_list_view(request, *args, **kwargs):
    
     qs = Post.objects.all()
     posts_list = [{"id": x.id, "content": x.content, "votes": random.randint(0, 100)} for x in qs]
     data = {
          "isUser": False,
          "response": posts_list
     }
     return JsonResponse(data)


def post_view(request, post_id, *args, **kwargs):
     
     data = {
          "id":post_id,
     }
     status = 200
     try:
          obj = Post.objects.get(id=post_id)
          data['content'] = obj.content
     except:
          data['message'] = "Not Found"
          status = 404

     
     return JsonResponse(data, status=status)

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