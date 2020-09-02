from django.contrib import admin
from .models import Post, Profile

from django.db import models
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    class Meta:
        model = Post

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'bio']
    class Meta:
        model = Profile

admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)