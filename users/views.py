from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, EmailTokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UserProfile
from .serializers import UserProfileSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {
                "full_name": f"{user.first_name} {user.last_name}",
                "email": user.email
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    
class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.serializer_class.get_user( request.data)
        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        try:
            profile = user.profile 
            profile_data = {
                "profile_image": profile.profile_image.url if profile.profile_image else None,
                "experience": profile.experience,
                "education_text": profile.education_text,
                "education_image": profile.education_image.url if profile.education_image else None,
                "skills": profile.skills,
                "languages": profile.languages,
                "resume": profile.resume.url if profile.resume else None,
                "resume_image": profile.resume_image.url if profile.resume_image else None,
                "role": profile.role,
            }
            user_data["profile"] = profile_data
        except UserProfile.DoesNotExist:
            pass


        return Response({
            "user": user_data,
            "refresh": response.data["refresh"],
            "access": response.data["access"],
        })