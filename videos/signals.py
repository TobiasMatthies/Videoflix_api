from django.dispatch import receiver
from django.db.models.signals import post_save
from . utils import convert_video
from . models import Video
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("video saved")
    if created:
       print("converting...")
       django_rq.enqueue(convert_video, instance.video_file.path, "hd1080")
       django_rq.enqueue(convert_video, instance.video_file.path, "hd720")
       django_rq.enqueue(convert_video, instance.video_file.path, "hd480")
