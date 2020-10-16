from django.shortcuts import get_object_or_404

from posts.models import Comment, Post

from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet

from .serializers import CommentSerializer, PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_object(self, *args, **kwargs):
        post_pk = self.kwargs.get('pk')
        try:
            if self.request.method == 'GET':
                post = get_object_or_404(Post, pk=post_pk)
            else:
                post = get_object_or_404(Post,
                                         pk=post_pk,
                                         author=self.request.user)
        except Exception:
            raise exceptions.PermissionDenied()
        self.check_object_permissions(self.request, post)
        return post

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_object(self, *args, **kwargs):
        comment_pk = self.kwargs.get('pk', 9)
        try:
            if self.request.method == 'GET':
                comment = get_object_or_404(Comment, pk=comment_pk)
            else:
                comment = get_object_or_404(Comment, pk=comment_pk,
                                            author=self.request.user)
        except Exception:
            raise exceptions.PermissionDenied()
        self.check_object_permissions(self.request, comment)
        return comment

    def perform_create(self, serializer, *args, **kwargs):
        id = self.kwargs.get('post')
        post = Post.objects.get(pk=id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self, *args, **kwargs):
        id = self.kwargs.get('post')
        post_obj = Post.objects.get(pk=id)
        return post_obj.comments
