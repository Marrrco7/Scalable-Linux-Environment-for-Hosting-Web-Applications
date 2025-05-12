from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title



class VideoGame(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    description = models.CharField(max_length=300)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Developer(models.Model):
    name = models.CharField(max_length=100)
    founded_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(VideoGame, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game.title} ({self.rating})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} Profile"


class Copy(models.Model):
    game = models.ForeignKey(VideoGame, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50, unique=True)
    condition = models.CharField(max_length=50)  #New, Used or Digital
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Copy of {self.game.title} ({self.serial_number})"
