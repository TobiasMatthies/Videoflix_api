from django.dispatch import receiver
from django.db.models.signals import post_save
from . utils import convert_video
from . models import Video

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("video saved")
    if created:
       print("converting...")
       convert_video(instance.video_file.path, "hd1080")
       convert_video(instance.video_file.path, "hd720")
       convert_video(instance.video_file.path, "hd480")
