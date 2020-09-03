from django.urls import path, re_path #url()
from . import views
from .views import (post_list_view, post_detail_view, post_create_view, post_update_view, post_delete_view)
from django.conf import settings
from django.conf.urls.static import static


app_name = 'main'  

urlpatterns = [
    path("", post_list_view.as_view(), name="home"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("post/create/", post_create_view.as_view(), name="post-create"),
    path("post/<int:pk>/", post_detail_view.as_view(), name='post-detail'),  #specifies the url for individual posts
    path("post/<int:pk>/update", post_update_view.as_view(), name='post-update'),
    path("post/<int:pk>/delete", post_delete_view.as_view(), name='post-delete'),
    path("profile/", views.profile, name= "profile")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)