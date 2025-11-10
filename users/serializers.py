from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    role = serializers.CharField(required=False, allow_blank=True) 
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'password2', 'role')

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with that email already exists."})
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        role = validated_data.pop('role', None) 
        validated_data.pop('password2')
        first_name, *last_name = full_name.split(' ', 1)
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=first_name,
            last_name=last_name[0] if last_name else '',
            password=validated_data['password']
           
        )
        profile, created = UserProfile.objects.get_or_create(user=user)
        if role:
            profile.role = role
            profile.save()
        return user


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    @classmethod
    def get_user(cls, data):
        User = get_user_model()
        try:
            return User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return None


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    education_image_url = serializers.SerializerMethodField()
  
    cv_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            "profile_image_url",
            "education_image_url",
           
            "cv_url",
            "profile_image",
            "education_image",
           
            "cv",
           
            "experience",
            "education_text",
            "skills",
            "languages",
            "role",
        ]

    def get_profile_image_url(self, obj):
        return obj.profile_image.url if obj.profile_image else None

    def get_education_image_url(self, obj):
        return obj.education_image.url if obj.education_image else None
    
    def get_cv_url(self, obj):
        return obj.cv.url if obj.cv else None
    
    
class RequestPasswordResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)