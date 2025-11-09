from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone
import datetime


def user_directory_path(instance, filename):
    # file name be named after user 
    return f'{instance.user.username}/{filename}'


class UserProfile(models.Model):
   
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    experience = models.TextField(blank=True, null=True)
    education_text = models.TextField(blank=True, null=True)
    
    languages = models.TextField(blank=True, null=True)
    cv = CloudinaryField('file', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    profile_image = CloudinaryField('image', blank=True, null=True)
    education_image = CloudinaryField('image', blank=True, null=True)

    # OTP fields for password reset
    password_reset_otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def otp_expired(self):
        if not self.otp_created_at:
            return True
        return timezone.now() > self.otp_created_at + datetime.timedelta(minutes=2)
