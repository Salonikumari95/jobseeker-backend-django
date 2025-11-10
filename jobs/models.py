from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

JOB_TYPE_CHOICES = (
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('internship', 'Internship'),
    ('contract', 'Contract'),
)

EXPERIENCE_CHOICES = (
    ('fresher', 'Fresher'),
    ('1-2', '1-2 years'),
    ('3-5', '3-5 years'),
    ('5+', '5+ years'),
)

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)

class JobPost(models.Model):
    title = models.CharField(max_length=255)
    job_description = models.TextField()
    location = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    company_logo = CloudinaryField('Company logo', blank=True, null=True)  
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    salary = models.CharField(max_length=50, blank=True, null=True)  
    category = models.CharField(max_length=50, blank=True, null=True)
    job_tags = models.CharField(max_length=255, blank=True, null=True)  
    required_experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, blank=True, null=True)
    required_skills = models.TextField(blank=True, null=True)
    required_education = models.TextField(blank=True, null=True)
    required_languages = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_posts')
    author_email = models.EmailField(blank=True, null=True)
    author_name = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.job_title


class JobApplication(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    cv = CloudinaryField('cv') 
    profile_image = CloudinaryField('profile_image')  
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # make a unique together constraint to prevent multiple applications to the same job by the same user
    def __str__(self):
        return f"{self.full_name} applied for {self.job.job_title}"
    # make a model to view my applications