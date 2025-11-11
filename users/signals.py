from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


# @receiver(post_save, sender=User)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created:  # Sirf jab new user create ho
#         subject = "Welcome to JobSeeker!"
#         message = f"Hi {instance.first_name},\n\nThank you for registering on JobSeeker portal. We are glad to have you on board!"
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [instance.email]

#         try:
#             send_mail(subject, message, from_email, recipient_list)
#         except Exception as e:
#             print(f"Error sending welcome email to {instance.email}: {e}")
            
