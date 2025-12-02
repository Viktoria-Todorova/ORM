
from django.db import models



class TennisPlayerManager(models.Manager):
    def get_tennis_players_by_wins_count(self):
        tennis_player = (self.annotate(wins=models.Count('matches')).filter(wins__gt=0)
                         .order_by('-wins','full_name').all())
        return tennis_player

