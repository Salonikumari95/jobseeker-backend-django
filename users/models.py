from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
        # file name be named after user 
        return f'{instance.user.username}/{filename}'
    
class UserProfile(models.Model):
   
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    education_text = models.TextField(blank=True, null=True)
    education_image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    languages = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    resume_image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    
   

    def __str__(self):
        return f"{self.user.username}'s profile"