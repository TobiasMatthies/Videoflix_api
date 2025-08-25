from rest_framework.response import Response
from django.http import FileResponse
from videos.models import Video
import subprocess
import os


def convert_video(source, resolution):
    """Converts a video file to mp4 and hls formats."""
    file_dir = os.path.dirname(source)
    file_name, file_ext = os.path.splitext(os.path.basename(source))
    new_file_name = f"{file_name}_{resolution}p.mp4"
    mp4_dir = os.path.join(file_dir, "mp4")
    os.makedirs(mp4_dir, exist_ok=True)
    new_file_path = os.path.join(mp4_dir, new_file_name)

    cmd = f"ffmpeg -i '{source}' -s {resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 '{new_file_path}'"
    run = subprocess.run(cmd, capture_output=True, shell=True)
    print(run.stderr)

    hls_file_name = f"hls_{file_name}_{resolution}p.m3u8"
    hls_dir = os.path.join(file_dir, "hls")
    os.makedirs(hls_dir, exist_ok=True)
    hls_file_path = os.path.join(hls_dir, hls_file_name)
    hls_file_cmd = f"ffmpeg -i '{new_file_path}' -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls '{hls_file_path}'"
    hls_run = subprocess.run(hls_file_cmd, capture_output=True, shell=True)
    print(hls_run.stderr)


def get_video_file(movie_id, **kwargs):
    """Returns a video file for streaming."""
    resolution = kwargs.get("resolution")
    segment = kwargs.get("segment")

    try:
        video = Video.objects.get(id=movie_id)
        video_path = video.video_file.path
        video_dir = os.path.dirname(video_path)

        hls_file_path = None
        content_type = None

        if resolution:
            content_type = "application/vnd.apple.mpegurl"
            hls_file_path = os.path.join(video_dir, "hls", f"hls_{os.path.splitext(os.path.basename(video_path))[0]}_hd{resolution}.m3u8")

        if segment:
            hls_file_path = os.path.join(video_dir, "hls", segment)
            content_type = "video/MP2T"
        print (hls_file_path)

        if os.path.exists(hls_file_path):
            return FileResponse(open(hls_file_path, "rb"), content_type=content_type)
        else:
            return Response({"error": "File not found"}, status=404)

    except Video.DoesNotExist:
        return Response({"error": "Video not found"}, status=404)
