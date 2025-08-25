from django.urls import path
from .views import VideoListAPIView, VideoPlaybackAPIView
urlpatterns = [
    path('video/', VideoListAPIView.as_view(), name='video-list'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoPlaybackAPIView.as_view(), name='video-playback'),
]
