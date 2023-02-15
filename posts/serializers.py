from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return self.context['request'].user == obj.owner

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'created_at', 'title', 'description',
            'image', 'is_owner'
        ]