from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from . utils import convert_video
from . models import Video
import django_rq
import os

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """Converts the video to different resolutions after it is saved."""
    print("video saved")
    if created:
       print("converting...")
       django_rq.enqueue(convert_video, instance.video_file.path, "hd1080")
       django_rq.enqueue(convert_video, instance.video_file.path, "hd720")
       django_rq.enqueue(convert_video, instance.video_file.path, "hd480")


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance: Video, **kwargs):
    """Deletes the video file and its converted versions when the video object is deleted."""
    if instance.video_file and os.path.isfile(instance.video_file.path):
        video_path = instance.video_file.path
        video_dir = os.path.dirname(video_path)
        video_filename_base = os.path.splitext(os.path.basename(video_path))[0]

        os.remove(video_path)

        subdirs_to_search = ['mp4', 'hls']

        for subdir in subdirs_to_search:
            search_dir = os.path.join(video_dir, subdir)
            if os.path.isdir(search_dir):
                for root, _, files in os.walk(search_dir):
                    for file in files:
                        if video_filename_base in file:
                            file_path_to_delete = os.path.join(root, file)
                            if os.path.isfile(file_path_to_delete):
                                os.remove(file_path_to_delete)
