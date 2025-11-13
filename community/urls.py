from .views import community_feed, create_community_post, like_post, comment_post
from django.urls import path

from .views import (
    CommunityPostListCreateAPIView,
    CommunityCommentListCreateAPIView,
    CommunityLikeAPIView,
)
# view endpoints
# urlpatterns= [
#     path('community/', community_feed, name='community-feed'),
#     path('community/create/', create_community_post, name='community-create'),
#     path('community/<int:post_id>/like/', like_post, name='community-like'),
#     path('community/<int:post_id>/comment/', comment_post, name='community-comment'),
# ]
# api endpoints

urlpatterns = [
    path('posts/', CommunityPostListCreateAPIView.as_view(), name='api-community-posts'),
    path('posts/<int:post_id>/comments/', CommunityCommentListCreateAPIView.as_view(), name='api-community-comments'),
    path('posts/<int:post_id>/like/', CommunityLikeAPIView.as_view(), name='api-community-like'),
]