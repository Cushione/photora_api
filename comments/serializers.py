from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    post = serializers.ReadOnlyField(source='post.id')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):
        return self.context['request'].user == obj.owner

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'post', 'created_at', 'content',
            'is_owner', 'profile_id', 'profile_image'
        ]