from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Post Serializer
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_name = serializers.ReadOnlyField(source="owner.profile.name")
    profile_image = serializers.ReadOnlyField(source="owner.profile.image.url")
    has_liked = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Is true when the request user is equal to the owner of the post
        """
        return self.context["request"].user == obj.owner

    def get_has_liked(self, obj):
        """
        Is true when the request user has liked the post
        """
        return obj.likes.filter(id=self.context["request"].user.id).exists()

    def validate_image(self, value):
        # Check if the image size is smaller than 2MB
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError("Image size is larger than 2MB!")
        # Check if the image height is smaller than 4096px
        if value.image.height > 4096:
            raise serializers.ValidationError(
                "Image height is larger than 4096px!"
            )
        # Check if the image width is smaller than 4096px
        if value.image.width > 4096:
            raise serializers.ValidationError(
                "Image width is larger than 4096px!"
            )
        return value

    class Meta:
        """
        Post Serializer Meta Data
        """

        model = Post
        fields = [
            "id",
            "owner",
            "created_at",
            "title",
            "description",
            "image",
            "is_owner",
            "profile_id",
            "profile_image",
            "profile_name",
            "has_liked",
            "number_of_likes",
            "number_of_comments",
        ]
