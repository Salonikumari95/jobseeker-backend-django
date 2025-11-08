from rest_framework import generics, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser
from .models import JobPost
from .serializers import JobPostSerializer


class JobPostListCreateView(generics.ListCreateAPIView):
    queryset = JobPost.objects.all().order_by('-created_at')
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location', 'company']
    ordering_fields = ['created_at', 'title']

    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)