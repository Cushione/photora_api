from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment Serializer
    """

    post = serializers.ReadOnlyField(source="post.id")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_name = serializers.ReadOnlyField(source="owner.profile.name")
    profile_image = serializers.ReadOnlyField(source="owner.profile.image.url")

    def get_is_owner(self, obj):
        """
        Is true when the request user is equal to the owner of the comment
        """
        return self.context["request"].user == obj.owner

    class Meta:
        """
        Comment Serializer Meta Data
        """

        model = Comment
        fields = [
            "id",
            "post",
            "created_at",
            "content",
            "profile_name",
            "is_owner",
            "profile_id",
            "profile_image",
        ]
