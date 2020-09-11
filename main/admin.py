from django.contrib import admin
from .models import Post, Profile, Follow, Comment, Upvote

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

class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'to_follow')
    class Meta:
        model = Follow

class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    class Meta:
        model = Upvote


admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Comment)
admin.site.register(Upvote, UpvoteAdmin)