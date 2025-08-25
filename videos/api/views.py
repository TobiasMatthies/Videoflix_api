from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.http import FileResponse
from videos.models import Video
from . serializers import VideoSerializer
from . permissions import IsAuthenticatedFromCookie
import os
from django.conf import settings

class VideoListAPIView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedFromCookie]


class VideoPlaybackAPIView(APIView):
    permission_classes = [IsAuthenticatedFromCookie]

    def get(self, request, *args, **kwargs):
        movie_id = kwargs.get("movie_id")
        resolution = kwargs.get("resolution")

        try:
            video = Video.objects.get(id=movie_id)
            video_path = video.video_file.path
            video_dir = os.path.dirname(video_path)

            hls_file_path = os.path.join(video_dir, f"hls_{os.path.splitext(os.path.basename(video_path))[0]}_hd{resolution}.m3u8")

            if os.path.exists(hls_file_path):
                content_type = "application/vnd.apple.mpegurl"
                return FileResponse(open(hls_file_path, "rb"), content_type=content_type)
            else:
                return Response({"error": "File not found"}, status=404)

        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)

class VideoSegmentView(APIView):
    permission_classes = [IsAuthenticatedFromCookie]

    def get(self, request, *args, **kwargs):
        movie_id = kwargs.get("movie_id")
        segment = kwargs.get("segment")

        try:
            video = Video.objects.get(id=movie_id)
            video_path = video.video_file.path
            video_dir = os.path.dirname(video_path)

            print(segment)
            hls_file_path = os.path.join(video_dir, segment)
            print (hls_file_path)

            if os.path.exists(hls_file_path):
                content_type = "video/MP2T"
                return FileResponse(open(hls_file_path, "rb"), content_type=content_type)
            else:
                return Response({"error": "File not found"}, status=404)

        except Video.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)
