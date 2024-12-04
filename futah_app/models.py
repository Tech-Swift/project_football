from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    is_coach = models.BooleanField(default=False)
    is_player = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Match(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches')
    date = models.DateField(auto_now=False, auto_now_add=False)
    opponent = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.coach} {self.date} {self.opponent} {self.location}"


class Player(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stats')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='matches')
    successful_passes = models.IntegerField(default=0)
    total_passes_attempted = models.IntegerField(default=0)
    passing_accuracy = models.FloatField(default=0.0)
    goals = models.IntegerField(default=0)
    position = models.CharField(max_length=10, default='0')
    assists = models.IntegerField(default=0)
    tackles = models.IntegerField(default=0)
    improvements = models.TextField(blank=True)

    def __str__(self):
        return f"stats for player{self.player}On the {self.match}"

    def calculate_passing_accuracy(self):
        if self.total_passes_attempted > 0:
            self.passing_accuracy = (self.successful_passes / self.total_passes_attempted) * 100
        else:
            self.passing_accuracy = 0.0
        self.save()
