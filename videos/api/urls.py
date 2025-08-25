from django.urls import path
from .views import VideoListAPIView, VideoPlaybackAPIView, VideoSegmentView
urlpatterns = [
    path('video/', VideoListAPIView.as_view(), name='video-list'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoPlaybackAPIView.as_view(), name='video-playback'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>', VideoSegmentView.as_view(), name='video-segment'),
]
