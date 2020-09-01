from django.db import models
from datetime import datetime
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    published = models.DateTimeField('date published', default=datetime.now)
    image = models.FileField(upload_to='images/', blank=True, null=True) #change to required later 

    def __str__(self):
        return self.title

