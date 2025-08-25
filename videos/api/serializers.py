from rest_framework import serializers
from videos.models import Video
from videos.models import Category


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for the Video model."""
    thumbnail_url = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Video
        fields = ["id", "created_at", "title", "description", "thumbnail_url", "category"]


    def get_thumbnail_url(self, obj):
        """Returns the absolute URL of the thumbnail."""
        request = self.context.get("request")
        if request is None:
            return None
        return request.build_absolute_uri(obj.thumbnail.url)
