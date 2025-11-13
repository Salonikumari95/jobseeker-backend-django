from rest_framework import serializers
from .models import CommunityPost, CommunityComment, CommunityLike

class CommunityPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = CommunityPost
        fields = ['id', 'author', 'content', 'media', 'created_at', 'likes_count', 'comments_count']

class CommunityCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CommunityComment
        fields = '__all__'
        read_only_fields = ['author', 'post', 'created_at']
        
class CommunityLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CommunityLike
        fields = ['id', 'post', 'user', 'created_at']