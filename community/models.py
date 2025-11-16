from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
class CommunityPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_posts')
    content = models.TextField()
    media = CloudinaryField('community-post', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CommunityComment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_spam = models.BooleanField(default=False)
    spam_confidence = models.FloatField(null=True, blank=True)
    is_profane = models.BooleanField(default=False)
    profanity_confidence = models.FloatField(null=True, blank=True)
    
class CommunityLike(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')