from django.contrib import admin

from .models import User, Player, Match


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_superuser', 'is_player')


list_filter = ('is_superuser', 'is_player')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('date', 'opponent', 'location', 'coach')
    list_filter = ('date', 'opponent', 'location', 'coach')
    search_fields = ('opponent', 'location')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player', 'match', 'passing_accuracy', 'goals', 'improvements')
    list_filter = ('match', 'player')
    search_fields = ('player__username', 'match__opponent')
