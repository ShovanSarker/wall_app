from rest_framework import viewsets
from wall.models import Writer
from wall.models import Post

from wall.serializers import WriterSerializer
from wall.serializers import PostSerializer


class WriterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Writer.objects.all()
    serializer_class = WriterSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows posts to be viewed.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
