from .models import CommunityPost, CommunityComment, CommunityLike
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.exceptions import PermissionDenied
from rest_framework import generics, permissions
from .models import CommunityPost, CommunityComment, CommunityLike
from .serializers import CommunityPostSerializer, CommunityCommentSerializer, CommunityLikeSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .utils import classify_comment
from django.core.paginator import Paginator
def community_feed(request):
    posts_list = CommunityPost.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    posts_with_comments = []
    for post in page_obj.object_list:
        comments_list = post.comments.all().order_by('created_at')
        comment_page_number = request.GET.get(f'comment_page_{post.id}', 1)
        comment_paginator = Paginator(comments_list, 3)
        comments_page_obj = comment_paginator.get_page(comment_page_number)
        # Use stored fields, do NOT call classify_comment here
        comments_with_badge = []
        for comment in comments_page_obj.object_list:
            comments_with_badge.append({
                'author': comment.author,
                'text': comment.text,
                'is_spam': comment.is_spam,
                'is_profane': comment.is_profane,
            })
        posts_with_comments.append({
            'post': post,
            'comments': comments_with_badge,
            'comments_page_obj': comments_page_obj,
        })

    return render(request, 'community/feed.html', {
        'posts_with_comments': posts_with_comments,
        'page_obj': page_obj,
    })
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
    like, created = CommunityLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    
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
        text = self.request.data.get('text', '')
        classification = classify_comment(text)
        serializer.save(
            author=self.request.user,
            post_id=post_id,
            is_spam=classification["is_spam"],
            spam_confidence=classification["spam_confidence"],
            is_profane=classification["is_profane"],
            profanity_confidence=classification["profanity_confidence"],
        )
class CommunityLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = CommunityPost.objects.get(id=post_id)
        like, created = CommunityLike.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Liked.'}, status=status.HTTP_201_CREATED)
    def delete(self, request, post_id):
        try:
            like = CommunityLike.objects.get(post_id=post_id, user=request.user)
            like.delete()
            return Response({'detail': 'Like removed.'}, status=status.HTTP_204_NO_CONTENT)
        except CommunityLike.DoesNotExist:
            return Response({'detail': 'Like not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class CommunityCommentRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CommunityComment.objects.all()
    serializer_class = CommunityCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete()
       

class CommunityPostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
           
            raise PermissionDenied("You can only delete your own posts.")
        instance.delete()
       
