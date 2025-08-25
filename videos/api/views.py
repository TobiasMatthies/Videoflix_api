from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from videos.models import Video
from . serializers import VideoSerializer
from . permissions import IsAuthenticatedFromCookie
from videos.utils import get_video_file

class VideoListAPIView(ListAPIView):
    """View to list all videos."""
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedFromCookie]


class VideoPlaybackAPIView(APIView):
    """View to play a video."""
    permission_classes = [IsAuthenticatedFromCookie]

    def get(self, request, *args, **kwargs):
        movie_id = kwargs.get("movie_id")
        resolution = kwargs.get("resolution")

        return get_video_file(movie_id, resolution=resolution)

class VideoSegmentView(APIView):
    """View to get a video segment for HLS streaming."""
    permission_classes = [IsAuthenticatedFromCookie]

    def get(self, request, *args, **kwargs):
        movie_id = kwargs.get("movie_id")
        segment = kwargs.get("segment")

        return get_video_file(movie_id, segment=segment)
