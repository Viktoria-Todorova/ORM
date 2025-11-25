from django.db import models


class AstronautManager(models.Manager):
    def get_astronauts_by_missions_count(self):
        astronauts = (self.annotate(astronauts_count=models.Count('missions_astronauts')).
                      order_by('-astronauts_count','phone_number'))
        return astronauts