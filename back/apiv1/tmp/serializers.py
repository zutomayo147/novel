from rest_framework import serializers
from posts.models import Post, Tag, Comment, Like, Saved_post

# from books.models import Book, Comment, Tag
from profiles.models import Profile
from accounts.models import User


#
# User
#
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )
        read_only_fields = (
            "username",
            "email",
        )


#
# Post
#
class TagRelatedField(serializers.RelatedField):
    """methodがいつ呼び出されるか不明？？"""

    def get_queryset(self):
        return Tag.objects.all()

    def to_internal_value(self, data):
        """tagがすでに登録されていないTagの時はcreate, ある時はget"""
        # data = {"content": "something"}
        tag, created = Tag.objects.get_or_create(**data)

        return tag

    def to_representation(self, value):
        return value.content


class PostSerializer(serializers.ModelSerializer):

    owner = UserSerializer(read_only=True)
    tagList = TagRelatedField(many=True, source="tags")

    class Meta:
        model = Post
        fields = [
            "id",
            "post_title",
            "owner" "post_caption",
            "post_content",
            "tagList",
        ]

    def create(self, validated_data):
        """tagを同時に追加できるようにする"""
        tags = validated_data.pop("tags", [])
        book = Post.objects.create(**validated_data)

        for tag in tags:
            book.tags.add(tag)

        return book


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment Model"""

    owner = UserSerializer(read_only=True)
    book = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "book", "owner"]


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag Model"""

    class Meta:
        model = Tag
        fields = ["id", "content"]


#
# Profile
#
class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile Model"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["user", "bio", "image"]
        read_only_fields = ("image",)


class ProfileImageSerializer(serializers.ModelSerializer):
    """Serializer for Profile Model"""

    user = UserSerializer(read_only=True)
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Profile
        fields = "__all__"