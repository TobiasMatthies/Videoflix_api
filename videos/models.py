from django.db import models

class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to="videos/")
    thumbnail = models.FileField(upload_to="thumbnails/", default="")
    category = models.CharField(max_length=100)
