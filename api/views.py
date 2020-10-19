from django.shortcuts import get_object_or_404

from posts.models import Comment, Post

from rest_framework import exceptions
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .serializers import CommentSerializer, PostSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer, *args, **kwargs):
        id = self.kwargs.get('post')
        post = get_object_or_404(Post, pk=id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self, *args, **kwargs):
        id = self.kwargs.get('post')
        post_obj = get_object_or_404(Post, pk=id)
        return post_obj.comments

