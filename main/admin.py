from django.contrib import admin
from .models import Post
from tinymce.widgets import TinyMCE
from django.db import models
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/date", {'fields': ["post_title", "post_published"]}),
        ("Content", {"fields": ["post_content"]})
    ]

    formfield_overrides= {
        models.TextField: {'widget': TinyMCE()},
    }

admin.site.register(Post, PostAdmin )