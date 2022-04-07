from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        fields = "__all__"
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
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
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

    def validate(self, data):
        """
        check that you can not subscribe to yourself
        """
        if self.context["request"].user == data["following"]:
            raise serializers.ValidationError(
                "You can't subscribe to yourself"
            )
        return data
