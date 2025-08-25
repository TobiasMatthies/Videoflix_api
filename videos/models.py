from django.db import models

class Category(models.Model):
    """Represents a video category."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    """Represents a video."""
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to="videos/")
    thumbnail = models.FileField(upload_to="thumbnails/", default="")
    category = models.ForeignKey(Category, related_name='videos', on_delete=models.SET_NULL, null=True)
