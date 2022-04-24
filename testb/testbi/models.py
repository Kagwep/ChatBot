from django.db import models
from embed_video.fields import EmbedVideoField

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=300)
    video = video = models.FileField(upload_to="video/%y")
    added = models.DateTimeField(auto_now_add=True)
    youtube_url = models.CharField(max_length=300) # same like models.URLField()
    def __str__(self) :
        return self.title

    class Meta:
        ordering = ['-added']