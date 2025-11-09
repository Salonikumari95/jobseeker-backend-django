from rest_framework import permissions

class IsRecruiter(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            hasattr(request.user, 'profile') and
            request.user.profile.role in ['recruiter', 'job_giver']
        )

class IsJobSeeker(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return (
            hasattr(request.user, 'profile') and
            request.user.profile.role == 'jobseeker'
        )