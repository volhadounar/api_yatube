from posts.models import Comment, Post

from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'image', 'pub_date', 'author')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'created', 'author', 'post')
        read_only_fields = ['post']
