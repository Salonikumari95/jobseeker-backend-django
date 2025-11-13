from .models import CommunityPost, CommunityComment, CommunityLike
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from .models import CommunityPost, CommunityComment, CommunityLike
from .serializers import CommunityPostSerializer, CommunityCommentSerializer, CommunityLikeSerializer

def community_feed(request):
    posts = CommunityPost.objects.all().order_by('-created_at')
    return render(request, 'community/feed.html', {'posts': posts})

@login_required
def create_community_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        media = request.FILES.get('media')
        CommunityPost.objects.create(author=request.user, content=content, media=media)
        return redirect('community-feed')
    return render(request, 'community/create_post.html')

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(CommunityPost, id=post_id)
    CommunityLike.objects.get_or_create(post=post, user=request.user)
    return redirect('community-feed')

@login_required
@require_POST
def comment_post(request, post_id):
    post = get_object_or_404(CommunityPost, id=post_id)
    text = request.POST.get('text')
    CommunityComment.objects.create(post=post, author=request.user, text=text)
    return redirect('community-feed')


class CommunityPostListCreateAPIView(generics.ListCreateAPIView):
    queryset = CommunityPost.objects.all().order_by('-created_at')
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination 
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
   


class CommunityCommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommunityCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return CommunityComment.objects.filter(post_id=post_id).order_by('created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)

class CommunityLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = CommunityPost.objects.get(id=post_id)
        like, created = CommunityLike.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Liked.'}, status=status.HTTP_201_CREATED)