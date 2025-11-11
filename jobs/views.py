
from rest_framework import generics
from rest_framework.exceptions import NotFound
from .serializers import JobPostSerializer, JobApplicationSerializer, BookmarkSerializer, MyApplicationDetailSerializer
from rest_framework import filters
from .models import JobPost, JobApplication, Bookmark
from .permisions import IsAuthorOrReadOnly, IsApplicantOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from users.permissions import IsRecruiter, IsJobSeeker


class JobPostCreateView(generics.CreateAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsRecruiter]
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            author=user,
            author_email=user.email,
            author_name=f"{user.first_name} {user.last_name}".strip() or user.username
        )


class JobPostListView(generics.ListAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['job_title',
                      'location',
                      'company_name',
                      'category',
                      'job_tags',
                      'required_skills',
                      'required_education',
                      'required_languages',
                      'required_experience',
                      'job_type',
                      'salary'] 


class JobApplicationCreateView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsJobSeeker]

    def perform_create(self, serializer):
        user = self.request.user
        job = serializer.validated_data['job']
       
        if JobApplication.objects.filter(applicant=user, job=job).exists():
            
            raise ValidationError("You have already applied to this job.")
        serializer.save(applicant=user)


class JobApplicationUpdateView(generics.UpdateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsRecruiter, IsAuthorOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        if obj.job.author != self.request.user:
            raise PermissionDenied("You are not allowed to update this application.")
        return obj


class JobPostUpdateView(generics.RetrieveUpdateAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    
    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise PermissionDenied("You are not allowed to update this job post.")
        return obj


class JobPostDeleteView(generics.DestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    
    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise PermissionDenied("You are not allowed to delete this job post.")
        return obj


class JobApplicationDeleteView(generics.DestroyAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsApplicantOrReadOnly]
     
    def get_object(self):
        obj = super().get_object()
        if obj.applicant != self.request.user:
            raise PermissionDenied("You are not allowed to delete this application.")
        return obj
    

class RecruiterJobApplicationsView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthorOrReadOnly] 

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        try:
            job = JobPost.objects.get(id=job_id)
        except JobPost.DoesNotExist:
            raise NotFound("Job not found.")

        if job.author != self.request.user:
            raise PermissionDenied("You are not allowed to view applications for this job.")

        return JobApplication.objects.filter(job=job).order_by('-applied_at')
    

class MyJobPostsView(generics.ListAPIView):
    serializer_class = JobPostSerializer
    permission_classes = [IsRecruiter] 

    def get_queryset(self):
        return JobPost.objects.filter(author=self.request.user)
    
    
class BookmarkCreateView(generics.CreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsJobSeeker]

    def perform_create(self, serializer):
        user = self.request.user
        job = serializer.validated_data['job']
        
       
        if Bookmark.objects.filter(user=user, job=job).exists():
            
            raise ValidationError("You have already bookmarked this job.")
        serializer.save(user=user)


class MyBookmarksView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsJobSeeker]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


class MyJobApplicationsView(generics.ListAPIView):
    serializer_class = MyApplicationDetailSerializer
    permission_classes = [IsJobSeeker]

    def get_queryset(self):
        return JobApplication.objects.filter(applicant=self.request.user)