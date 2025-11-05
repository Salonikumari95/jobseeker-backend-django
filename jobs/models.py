from django.db import models
from django.contrib.auth.models import User

class JobPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    company = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_posts')

    def __str__(self):
        return self.title