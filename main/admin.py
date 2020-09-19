from django.contrib import admin
from .models import Post, Profile, Follow, Comment, Upvote, Message, Conversation

from django.db import models
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'ticker', 'date_traded','tags']
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

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content', 'created_date')
    class Meta:
        model = Comment

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'text', 'date_sent', 'conversation']
    class Meta:
        model = Message



admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Upvote, UpvoteAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Conversation)
