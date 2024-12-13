from django.urls import reverse
from django.db import models
from accounts.models import CustomUser

class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    team = models.CharField(max_length=100)
    position = models.CharField(max_length=50, null=True, blank=True)
    coach = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='players')
    picture = models.ImageField(upload_to='player_pics/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('players:player_detail', kwargs={'pk': self.pk})
