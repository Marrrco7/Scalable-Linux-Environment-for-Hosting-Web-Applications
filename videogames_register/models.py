from django.db import models


# Create your models here.

class Genre(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class VideoGame(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    description = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
