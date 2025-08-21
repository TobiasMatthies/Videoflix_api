from django.urls import path
from .views import VideoListAPIView, VideoPlaybackAPIView
urlpatterns = [
    path('video/', VideoListAPIView.as_view(), name='video-list'),
    path('video/<int:movie_id>/<str:resolution>/<str:file_name>', VideoPlaybackAPIView.as_view(), name='video-playback'),
]
