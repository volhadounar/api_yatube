from django.shortcuts import get_object_or_404

from posts.models import Comment, Post

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import CommentSerializer, PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, pk, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = get_object_or_404(Post, pk=pk, author=request.user)
        except Exception:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance,
                                         data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            post_obj = get_object_or_404(Post, pk=pk, author=request.user)
        except Exception:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(post_obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(CreateAPIView, ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, post):
        self.post_id = post
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.post_id)
        serializer.save(author=self.request.user, post=post)

    def list(self, request, post):
        post_obj = Post.objects.get(pk=post)
        queryset = Comment.objects.filter(post=post_obj)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.filter()
    serializer_class = CommentSerializer

    def update(self, request, post, pk, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = get_object_or_404(Comment, pk=pk, author=request.user)
        except Exception:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance,
                                         data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, post, pk):
        try:
            instance = get_object_or_404(Comment, pk=pk, author=request.user)
        except Exception:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
