from django.contrib import admin
from .models import Post

from django.db import models
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)