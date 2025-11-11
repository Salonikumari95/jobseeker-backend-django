from rest_framework import serializers
from .models import JobPost, JobApplication, Bookmark
from django.contrib.auth.models import User
from users.models import UserProfile
from cloudinary.models import CloudinaryField

class JobPostSerializer(serializers.ModelSerializer):
    company_logo_url = serializers.SerializerMethodField()
    class Meta:
        model = JobPost
        fields = ['id','author', 'author_email', 'author_name', 'title', 'job_description', 'location', 'company_name', 'company_logo', 'company_logo_url', 'job_type', 'salary', 'category', 'job_tags', 'required_experience', 'required_skills', 'required_education', 'required_languages', 'created_at','company_logo_url']
        read_only_fields = ['author', 'created_at', 'updated_at']
    def get_company_logo_url(self, obj):
        return obj.company_logo.url if obj.company_logo else None


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['applicant', 'applied_at']

    
    def get_author_name(self, obj):
        full_name = f"{obj.author.first_name} {obj.author.last_name}".strip()
        return full_name if full_name else obj.author.username
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

       
        if instance.job.author == user:
            allowed = {'status'}
            for key in list(validated_data.keys()):
                if key not in allowed:
                    validated_data.pop(key)
      
        elif instance.applicant == user:
            if 'status' in validated_data:
                validated_data.pop('status')
        else:
           
            raise serializers.ValidationError("You do not have permission to update this application.")

        return super().update(instance, validated_data)
    

class BookmarkSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Bookmark
        fields = ['id', 'job', 'created_at']

class MyApplicationDetailSerializer(serializers.ModelSerializer):
    job = JobPostSerializer(read_only=True)  

    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'status', 'applied_at', 'full_name', 'email', 'phone', 'cv', 'profile_image']
        read_only_fields = ['job', 'status', 'applied_at']
