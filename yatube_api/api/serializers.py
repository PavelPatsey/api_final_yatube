from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


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
        required=False,
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
    )
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        fields = ("user", "following")
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=["user", "following"]
            )
        ]

    # def validate(self, data):
    #     """
    #     check that you can not subscribe to yourself
    #     """
    #     # breakpoint()
    #     user = self.context["request"].user
    #     following = data.username
    #     # breakpoint()
    #     if user == following:
    #         raise serializers.ValidationError("You can't subscribe to yourself")
    #     return data
