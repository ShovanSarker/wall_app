from rest_framework import serializers

from wall.models import Writer
from wall.models import Post


class WriterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Writer
        fields = ['url', 'name', 'email', 'username', 'created_at', 'is_active']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['url', 'title', 'writer', 'content', 'created_at']
