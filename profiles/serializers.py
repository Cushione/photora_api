from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return self.context['request'].user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'name', 'content', 'image', 'is_owner'
        ]


class ProfileListSerializer(serializers.ModelSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')
    is_followed = serializers.SerializerMethodField()

    def get_is_followed(self, obj):
        return obj.profile.followers.filter(id=self.context['request'].user.id).exists()

    class Meta:
        model = User
        read_only_fields = ['username']
        fields = [
            'profile_id', 'profile_image', 'is_followed'
        ]