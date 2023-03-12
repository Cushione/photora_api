from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile Serializer
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()

    def get_is_followed(self, obj):
        """
        Is true when the request user is following the profile
        """
        return obj.followers.filter(
            id=self.context["request"].user.id
        ).exists()

    def get_is_owner(self, obj):
        """
        Is true when the request user is equal to the owner of the profile
        """
        return self.context["request"].user == obj.owner

    class Meta:
        """
        Profile Serializer Meta Data
        """

        model = Profile
        fields = [
            "id",
            "owner",
            "created_at",
            "name",
            "content",
            "image",
            "is_owner",
            "is_followed",
        ]


class ProfileListSerializer(serializers.ModelSerializer):
    """
    Profile Serializer for lists
    """

    profile_id = serializers.ReadOnlyField(source="profile.id")
    profile_image = serializers.ReadOnlyField(source="profile.image.url")
    profile_name = serializers.ReadOnlyField(source="profile.name")
    is_owner = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()

    def get_is_followed(self, obj):
        """
        Is true when the request user is following the profile
        """
        return obj.profile.followers.filter(
            id=self.context["request"].user.id
        ).exists()

    def get_is_owner(self, obj):
        """
        Is true when the request user is equal to the owner of the profile
        """
        return self.context["request"].user == obj

    class Meta:
        """
        Profile Serializer Meta Data
        """

        model = User
        fields = [
            "profile_id",
            "profile_image",
            "profile_name",
            "is_followed",
            "is_owner",
        ]
