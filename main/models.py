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
    

    def __str__(self):
        return f'{self.user.username} Profile'

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE) #tie follows to one user
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('follower', 'following')

