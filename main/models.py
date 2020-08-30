from django.db import models
from datetime import datetime
# Create your models here.
class Post(models.Model):
    post_title = models.CharField(max_length=200)
    post_content = models.TextField()
    post_published = models.DateTimeField('date published', default=datetime.now)

    def __str__(self):
        return self.post_title