from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Message, Follow, Comment
from notifications.signals import notify

@receiver(post_save, sender=User) # create user profile when user creates his account
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User) # update user profile
def save_profile(sender, instance, **kwargs):
    instance.profile.save()



#comment notifications
@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if instance.post.user != instance.user:     #check to see if user is commenting on own post, if so then no notifcations
        if created:
            notify.send(
                sender=instance.user,
                recipient=instance.post.user,
                verb='commented',
                action_object=instance,
                target=instance.post,
                description='{instance.user} has commented your post',
            )

#follow notification
@receiver(post_save, sender=Follow)
def notify_follow(sender, instance, created, **kwargs):
    if created:
        notify.send(
            sender=instance.user,
            recipient=instance.to_follow,
            verb='followed',
            action_object=instance,
            target=instance.to_follow,
            description='{instance.user} has followed you',
        )

#message notification
@receiver(post_save, sender=Message)
def notify_message(sender, instance, created, **kwargs):
    if created:
        notify.send(
            sender=instance.sender,
            recipient=instance.recipient,
            verb='messaged',
            action_object=instance,
            target=instance.recipient,
            description='{instance.user} has messaged you',
        )
