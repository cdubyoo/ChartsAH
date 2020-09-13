from django.urls import path, re_path #url()
from . import views
from .views import (post_list_view, post_detail_view, post_create_view, post_update_view, post_delete_view, user_posts, feed_list_view, search_view)
from django.conf import settings
from django.conf.urls.static import static


app_name = 'main'  
#call upon the function from view and links it to url path
urlpatterns = [
    path("", post_list_view.as_view(), name="home"),
    path("feed/", feed_list_view.as_view(), name="feed"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("post/create/", post_create_view.as_view(), name="post-create"),
    path("post/<int:pk>/", post_detail_view.as_view(), name='post-detail'),  #specifies the url for individual posts
    path("post/<int:pk>/update", post_update_view.as_view(), name='post-update'),
    path("post/<int:pk>/delete", post_delete_view.as_view(), name='post-delete'),
    path("profile/", views.profile, name= "profile"),
    path("user/<str:username>", user_posts.as_view(), name="user-posts"), #profile view
    path("upvote", views.upvote, name='upvote-post'), 
    path("search/", search_view.as_view(), name='search')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)