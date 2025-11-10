from django.contrib import admin
from .models import JobPost, JobApplication
# Register your models here.
admin.site.register(JobPost)
admin.site.register(JobApplication)