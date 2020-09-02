from django.urls import path, re_path #url()
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'main'  

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("create-post/", views.post_create_view, name="create-post"),
    path("posts/", views.post_list_view),
    path("posts/<int:post_id>", views.post_view),
    path("profile/", views.profile, name= "profile")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)