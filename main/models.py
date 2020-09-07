from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL 
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #many to one relationship where many posts can be tied to one user
    content = models.TextField(blank=True, null=True) # change blank later
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.FileField(upload_to='images/', blank=True, null=True) #change to required later 

    def __str__(self):
        return self.content
    # sets the redirect to the new specific post's absolute path
    def get_absolute_url(self):
        return reverse('main:post-detail', kwargs={'pk': self.pk})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')  #add in later
    bio = models.TextField(max_length=1000, blank=True)

    @property
    def followers(self):
        return Follow.objects.filter(to_follow=self.user).count() #count of followers by filtering user and to_follow count

    @property
    def following(self):
        return Follow.objects.filter(user=self.user).count() #count of followers by filtering user and its user(following) count

    def __str__(self):
        return f"{self.user.username}'s Profile"



class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE) #tie follows to one user
    to_follow = models.ForeignKey(User, related_name='to_follow',  on_delete=models.CASCADE)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) #tie post model to comments as a one to many relationship using foreign key
    user = models.ForeignKey(User, related_name='commented_user', on_delete=models.CASCADE) #tie to user posting
    created_date = models.DateTimeField(default=timezone.now)
    content = models.TextField(max_length=120)

    def __str__(self):
        return self.comment


