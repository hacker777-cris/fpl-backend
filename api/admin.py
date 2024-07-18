from django.contrib import admin
from .models import Fixture, GameweekStats, Team, Player, PlayerPosition

fixtures = admin.site.register(Fixture)
teams = admin.site.register(Team)
players = admin.site.register(Player)
player_positions = admin.site.register(PlayerPosition)
game_week_stats = admin.site.register(GameweekStats)
