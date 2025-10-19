from django.db import models


class RoomTypeChoices(models.TextChoices):
    STANDARD = 'Standard','Standard'
    DELUXE = 'Deluxe','Deluxe'
    SUITE = 'Suite','Suite'

class CharactersChoices(models.TextChoices):
    #"Mage", Warrior", "Assassin", and "Scout"
    MAGE = 'Mage','Mage'
    WARRIOR = 'Warrior','Warrior'
    ASSASSIN = 'Assassin','Assassin'
    SCOUT = 'Scout','Scout'
    FUSION = 'Fusion','Fusion'