from rest_framework.generics import ListAPIView
from videos.models import Video
from . serializers import VideoSerializer
from . permissions import IsAuthenticatedFromCookie


class VideoListAPIView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedFromCookie]
