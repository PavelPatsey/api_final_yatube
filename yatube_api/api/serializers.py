from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        fields = ("id", "text", "author", "image", "group", "pub_date")
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )
    post = serializers.PrimaryKeyRelatedField(
        required=False,
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ("id", "author", "post", "text", "created")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title", "slug", "description")
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    following = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        fields = ("id", "user", "following")
        model = Follow
