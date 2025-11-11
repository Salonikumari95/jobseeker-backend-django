from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    EmailTokenObtainPairSerializer,
    UserProfileSerializer,
    RequestPasswordResetOTPSerializer,
    PasswordResetSerializer
)
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UserProfile

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError

import random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


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
                "email": user.email,
                "role": user.profile.role if hasattr(user, 'profile') else None,
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
        user = self.serializer_class.get_user(request.data)
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
                "cv": profile.cv.url if profile.cv else None,
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


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RequestPasswordResetOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            profile.password_reset_otp = otp
            profile.otp_created_at = timezone.now()
            profile.save()
            
            try :
                send_mail(
                subject="Your Password Reset OTP",
                message=f"Your OTP for password reset is: {otp}. It expires in 2 minutes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            except Exception as e:
                print(f"Error sending email: {e} otp is {otp}")
                

            return Response({"detail": "OTP sent to email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        if new_password != confirm_password:
            return Response({"password": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            profile = user.profile

            # Check OTP and expiration
            if profile.password_reset_otp != otp:
                return Response({"otp": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            if profile.otp_expired():
                return Response({"otp": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            user.set_password(new_password)
            user.save()

            # Clear OTP fields
            profile.password_reset_otp = None
            profile.otp_created_at = None
            profile.save()

            return Response({"detail": "Password reset successful."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
