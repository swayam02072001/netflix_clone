from django.db import models
import uuid
from django.conf import settings
# Create your models here.
class Genre(models.Model):
    GENRE_CHOICES = models.CharField(primary_key =True,max_length=100)

    def __str__(self):
        return self.GENRE_CHOICES
    
class Movie(models.Model):

    uu_id = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=250)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE)   
    length = models.PositiveIntegerField()
    image_card = models.ImageField(upload_to='movie_images/') 
    image_cover = models.ImageField(upload_to='movie_images/') 
    video = models.FileField(upload_to='movie_videos/')
    movie_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class Movielist(models.Model):
    owner_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    