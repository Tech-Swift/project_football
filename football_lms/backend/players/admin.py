from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'age', 'coach')
    search_fields = ('name', 'team', 'coach__username')
