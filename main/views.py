from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Post, Profile, Follow, Comment, Upvote, Message, Conversation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm, PostForm, UserUpdateForm, ProfileUpdateForm, CommentForm, MessageForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Exists, OuterRef, Q, Max
from .filters import PostFilter 
from datetime import datetime, timedelta, date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django_filters.views import FilterView
from django.views.generic.edit import ModelFormMixin


ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# function based views handle the logic for the route and render the template.
# class based views handle backend logic using generic views and inherit from mixins





class search_filter_view(FilterView):
     template_name = 'main/search_filter.html'
     paginate_by = 2
     ordering = ['total_upvotes']
     filterset_class = PostFilter

     


     '''
     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset().distinct())
          return context
'''
'''
     def get_form(self):
          form = super(search_filter_view, self).get_form()
          form.fields['date_traded'].widget.attrs.update({'class': 'datepicker'})
          form.fields['tags'].widget.attrs.update({'data-role':'tagsinput'})
          print('worked')
          return form
'''
     



class search_view(ListView):
    template_name = 'main/search.html'
    context_object_name = 'posts'
    paginate_by = 2
     # searches through everything using Q import 
    def get_queryset(self, *args, **kwargs):
          q = self.request.GET.get('q')
          order_by = self.request.GET.get('order_by', '-date_traded') #adding parameters to be called on in the template
          self.posts = Post.objects.filter(
             Q(ticker__icontains=q) |
             #Q(user__username__icontains=q) |
             #Q(content__icontains=q) |
             Q(tags__name__icontains=q) 
          ).annotate(
               upvoted=Exists(Post.upvotes.through.objects.filter( #upvoted is called in the template using if statement
                    user_id=self.request.user.id,
                    post_id=OuterRef('pk')
            ))).order_by(order_by)
          return self.posts


class conversation_view(ListView):
     model = Message
     template_name = 'main/conversations_list.html'
     context_object_name = 'conversations'


     def get_context_data(self, *args, **kwargs):
          current_user = self.request.user
          context = super().get_context_data(*args, **kwargs)
          conversations = Conversation.objects.filter(participants=current_user)
          context['conversations'] = conversations
          

          return context

         
          



from itertools import chain



class message_view(CreateView):
     model = Message
     template_name = 'main/conversations.html'
     form_class = MessageForm
    

     def get_context_data(self, *args, **kwargs):
          # get displayed user context
          displayed_user = get_object_or_404(User, username=self.kwargs.get('username'))
          context = super(message_view, self).get_context_data(**kwargs)
          context['user_profile'] = Profile.objects.filter(user=displayed_user)

          # get convo list context
          current_user = self.request.user
          context['conversations'] = Conversation.objects.filter(participants=current_user)

          # get messages

          sent_messages = Message.objects.filter(sender=current_user).filter(recipient=displayed_user).order_by('date_sent')
          receieved_messages = Message.objects.filter(recipient=current_user).filter(sender=displayed_user).order_by('date_sent')


          messages = list(chain(sent_messages, receieved_messages))

          messages.sort(key=lambda message: message.date_sent)

          print(messages)
          context['messages'] = messages
          #context['receieved_messages'] = receieved_messages
          #context['sent_messages'] = sent_messages



          return context
   

     def post(self, request, *args, **kwargs):
          form = MessageForm(request.POST)

          displayed_user = get_object_or_404(User, username=self.kwargs.get('username'))
          current_user = self.request.user
          
          if form.is_valid():

               user_convo = Conversation.objects.filter(participants=displayed_user).filter(participants=current_user) 
               # ^^ chain filter by first then second user
               
               # checking if there is already convo established, if not create convo
               if user_convo.count() == 0:
                    conversation = Conversation.objects.create()
                    conversation.participants.add(request.user)
                    conversation.participants.add(displayed_user)
                    message = Message(text=request.POST.get('text'),
                                   sender=current_user, recipient=displayed_user,
                                   conversation=conversation)
                    message.save()
                    # set lastmsg with text from post request since there is no convo prior
                    user_convo.update(last_message=request.POST.get('text'))

               #if there is already convo, then add message into the convo
               else:
                    message = Message(text=request.POST.get('text'), #this is creating Message()
                                   sender=current_user, recipient=displayed_user,
                                   conversation=user_convo[0]) #conversation[0] would be the first object in the queryset
                    message.save()

                    # last message by filtering for top object from 2 users [:1] returns only 1 object
                    sent = Message.objects.filter(sender=current_user).filter(recipient=displayed_user).order_by('-date_sent')[:1]
                    received = Message.objects.filter(recipient=current_user).filter(sender=displayed_user).order_by('-date_sent')[:1]
                    lastmsg = list(chain(sent, received))
                    user_convo.update(last_message=lastmsg[0].text) #pulling text from object and updating convo
                    
                    return redirect('main:message', username=displayed_user)                      
          return redirect('main:message', username=displayed_user)



# creating posts
class post_create_view(LoginRequiredMixin, CreateView):

     
     model = Post
     fields = ['content', 'image', 'ticker', 'date_traded', 'tags']
     
     #override createview fields and change attributes for script access
     def get_form(self):
          form = super(post_create_view, self).get_form()
          today = date.today()
          form.fields['date_traded'].widget.attrs.update({'class': 'datepicker'})
          form.fields['tags'].widget.attrs.update({'data-role':'tagsinput'})
          return form
     #set user to 'logged in user' then validate the form
     def form_valid(self, form):
          form.instance.user = self.request.user
          return super().form_valid(form)
     
# update view
class post_update_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
     model = Post
     fields = ['content', 'image','ticker', 'date_traded', 'tags']
     #set user to logged in user then validate the form
     def form_valid(self, form):
          form.instance.user = self.request.user
          return super().form_valid(form)

     def test_func(self):
          post = self.get_object() # get the post 
          if self.request.user == post.user:
               return True
          return False



# list of all posts sorted by new
class post_list_view(ListView):
    
     model = Post
     template_name = 'main/home.html'
     paginate_by = 5
     context_object_name = 'posts' # used for object name to be looped through 
     ordering = ['-date_posted']

     
     # using Exists() subquery to check if table exists between user, post, and upvotes
     def get_queryset(self, *args, **kwargs):
          return super().get_queryset(*args, **kwargs).annotate(
               upvoted=Exists(Post.upvotes.through.objects.filter( #upvoted is called in the template using if statement
                    user_id=self.request.user.id,
                    post_id=OuterRef('pk')
            )))
 

# sort by all time top
class top_all(ListView):
     model = Post
     template_name = 'main/home.html'
     context_object_name = 'posts'
     ordering = ['-total_upvotes'] # order by total upvotes
     paginate_by = 5

     # using Exists() subquery to check if table exists between user, post, and upvotes. to show if user has already upvoted posts
     def get_queryset(self, *args, **kwargs):
          return super().get_queryset(*args, **kwargs).annotate(
               upvoted=Exists(Post.upvotes.through.objects.filter( #upvoted is called in the template using if statement
                    user_id=self.request.user.id,
                    post_id=OuterRef('pk')
            )))


class top_day(ListView):     
     model = Post
     template_name = 'main/home.html'
     context_object_name = 'posts'
     paginate_by = 5

     def get_queryset(self):
          today = date.today()
          return Post.objects.filter(date_traded__gte=today).annotate(
               # ^^ using the '__in' syntax to make query to ask for posts with user = follows, which is array of users who is followed by current user
               upvoted=Exists(Post.upvotes.through.objects.filter( 
               user_id=self.request.user.id,
               post_id=OuterRef('pk')))).order_by('-total_upvotes')


class top_week(ListView):     
     model = Post
     template_name = 'main/home.html'
     context_object_name = 'posts'
     paginate_by = 5


     def get_queryset(self):
          one_week_ago = datetime.today() - timedelta(days=7)
          return Post.objects.filter(date_traded__gte=one_week_ago).annotate(
               # ^^ using the '__in' syntax to make query to ask for posts with user = follows, which is array of users who is followed by current user
               upvoted=Exists(Post.upvotes.through.objects.filter( 
               user_id=self.request.user.id,
               post_id=OuterRef('pk')))).order_by('-total_upvotes')


class top_month(ListView):     
     model = Post
     template_name = 'main/home.html'
     context_object_name = 'posts'
     paginate_by = 5

     def get_queryset(self):
          one_month_ago = datetime.today() - timedelta(days=30)
          return Post.objects.filter(date_traded__gte=one_month_ago).annotate(
               # ^^ using the '__in' syntax to make query to ask for posts with user = follows, which is array of users who is followed by current user
               upvoted=Exists(Post.upvotes.through.objects.filter( 
               user_id=self.request.user.id,
               post_id=OuterRef('pk')))).order_by('-total_upvotes')         

class top_year(ListView):     
     model = Post
     template_name = 'main/home.html'
     context_object_name = 'posts'
     paginate_by = 5

     def get_queryset(self):
          one_year_ago = datetime.today() - timedelta(days=365)

          return Post.objects.filter(date_traded__gte=one_year_ago).annotate(
               # ^^ using the '__in' syntax to make query to ask for posts with user = follows, which is array of users who is followed by current user
               upvoted=Exists(Post.upvotes.through.objects.filter( 
               user_id=self.request.user.id,
               post_id=OuterRef('pk')))).order_by('-total_upvotes')         





# feed of user's followings
class feed_list_view(LoginRequiredMixin, ListView):
    
     model = Post
     template_name = 'main/home.html'
     context_object_name = 'posts' # this is called from the html as 'for post in posts'
     ordering = ['-date_posted'] # minus to reverse the date posted, so newer posts show up on top
     paginate_by = 2 #sets pagination per page

     
     def get_queryset(self): #function to return a queryset(list of items) 
          user = self.request.user #specify user as current user who is sending request
          qs = Follow.objects.filter(user=user) #query set filtering by current user's follow table
          follows = [user] # store following users as an array as 'follows'
          for users in qs: #iterate through the query set with a for loop
               follows.append(users.to_follow) #add to array the users who are in the to_follow list of the user's follow table model
          return Post.objects.filter(user__in=follows).annotate(
               # ^^ using the '__in' syntax to make query to ask for posts with user = follows, which is array of users who is followed by current user
               upvoted=Exists(Post.upvotes.through.objects.filter(  
               # ^^ using Exists() subquery to check if table exists between user, post, and upvotes. to show if user has already upvoted posts     
               user_id=self.request.user.id,
               post_id=OuterRef('pk')))).order_by('-date_posted') 


#individual post view
class post_detail_view(DetailView):
     model = Post
     template_name = 'main/post_detail.html'
     context_object_name = 'post'

     # render upvote status
     def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).annotate(
            upvoted=Exists(Post.upvotes.through.objects.filter( #upvoted is called in the template using if statement
                user_id=self.request.user.id,
                post_id=OuterRef('pk')
            ))
        )

     # render comment form
     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['form'] = CommentForm(instance=self.request.user) 

          return context

     def post(self, request, *args, **kwargs):
          create_comment = Comment(content=request.POST.get('content'),
                                   user=self.request.user, post=self.get_object())
          create_comment.save()
     
          return self.get(self, request, *args, **kwargs)


class post_delete_view(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
     model = Post
     success_url = '/' #redirect to home if delete success
     def test_func(self):
          post = self.get_object() # get the post 
          if self.request.user == post.user:
               return True
          return False


class user_posts(LoginRequiredMixin, ListView):
    
     model = Post
     template_name = 'main/user_posts.html'
     context_object_name = 'posts'
     paginate_by = 5 #sets pagination per page

     def displayed_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username')) # user on display

     #get data from model and filter by user
     def get_queryset(self):
          user = get_object_or_404(User, username =self.kwargs.get('username'))
          return Post.objects.filter(user=user).order_by('-date_posted')

     #override and get data from another model
     def get_context_data(self, **kwargs):
          displayed_user = get_object_or_404(User, username =self.kwargs.get('username'))
          current_user = self.request.user

          if current_user is None:
               followable = False
          else:
               followable = (Follow.objects.filter(user=current_user, to_follow=displayed_user).count() == 0)

          context = super(user_posts, self).get_context_data(**kwargs)
          context['user_profile'] = Profile.objects.filter(user=displayed_user)
          context['followable'] = followable
          return context

     #post request, done as def post because its inside a class
     def post(self, request, *args, **kwargs):
          follows_between = Follow.objects.filter(user = request.user, to_follow = self.displayed_user()) # filter out current user and displayed user as a variable
          if 'follow' in request.POST: # calling the post request from template attribute name=follow
               new_relation = Follow(user=request.user, to_follow=self.displayed_user()) #filter new relation with request user and displayed user using Follow model
               if follows_between.count() == 0: # if there is no count/relation between the 2, then save new relation
                    new_relation.save() 
          # doing the reverse for if the post request is from html name=unfollow
          elif 'unfollow' in request.POST: 
               new_relation = Follow(user=request.user, to_follow=self.displayed_user()) 
               if follows_between.count() > 0: # if  there is count/relation between the 2, then delete relation
                    follows_between.delete() 

          return self.get(self, request, *args, **kwargs)




class following_view(ListView):
     model = Follow
     template_name = 'main/following.html'
     context_object_name = 'follows'

     def displayed_user(self):
          return get_object_or_404(User, username=self.kwargs.get('username')) # user on display

     def get_queryset(self):
          user = self.displayed_user()
          return Follow.objects.filter(user=user) #.order_by('-date')

     # check to render the following section of the template
     def get_context_data(self, *args, **kwargs):
          # use of super is to add new value to context without losing the default view's context values
          context = super().get_context_data(**kwargs) 
          context['follow'] = 'following'
          return context


class follower_view(ListView):
     model = Follow
     template_name = 'main/following.html'
     context_object_name = 'follows'

     def displayed_user(self):
          return get_object_or_404(User, username=self.kwargs.get('username')) # user on display

     def get_queryset(self):
          user = self.displayed_user()
          return Follow.objects.filter(to_follow=user) #.order_by('-date')

     # check to render the following section of the template
     def get_context_data(self, *args, **kwargs):
          # use of super is to add new value to context without losing the default view's context values
          context = super().get_context_data(**kwargs) 
          context['follow'] = 'followers'
          return context








def upvote(request):
     if request.POST.get('action') == 'post':
          result = ''
          id = request.POST.get('postid')
          post = get_object_or_404(Post, id=id) #grabbing the selected post using postid
          new_relation = Upvote(user=request.user, post=post) #storing the upvote relation between user and post using Upvote model arguments - 'user' and 'post'
          if post.upvotes.filter(id=request.user.id).exists(): #checking if user already has upvote relations with post by filtering user and post
               post.upvotes.remove(request.user) #remove upvote relation from post 
               post.total_upvotes -= 1 #minus 1 total_upvotes from post
               result = post.total_upvotes #storing the new total_upvotes into result
               Upvote.objects.filter(user=request.user, post=post).delete() #filtering user and post and deleting the upvote table
               post.save()
          else:
               post.upvotes.add(request.user)
               post.total_upvotes += 1
               result = post.total_upvotes
               new_relation.save()  
               post.save()

          return JsonResponse({'result': result, }) # return the new total_vote count back to html as json


# register
def register(request):
     if request.method == "POST":
          form = NewUserForm(request.POST)
          if form.is_valid():
               user = form.save() # saving the user 
               username = form.cleaned_data.get('username')
               messages.success(request, f"New user created: {username}")
               login(request, user)
               messages.info(request, f"Welcome, {username}.")
               return redirect("main:home")

          else:

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
     return redirect("main:home")

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

@login_required
def profile(request):
     if request.method == "POST":
          u_form = UserUpdateForm(request.POST, instance=request.user)
          p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

          if u_form.is_valid and p_form.is_valid():
               u_form.save()
               p_form.save()
               messages.success(request, f'Your profile has been updated.')
               return redirect('main:profile')
     else:
          u_form = UserUpdateForm(instance=request.user)
          p_form = ProfileUpdateForm(instance=request.user.profile)

     context = {
          'u_form': u_form,
          'p_form': p_form
     }
     
     return render(request, 'main/profile.html', context)






