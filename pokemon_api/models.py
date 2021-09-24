from django.db import models


# Create your models here.
class Pokemon(models.Model):
    """Database model for pokemon information"""
    id_pokemon = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    weight = models.IntegerField()
    height = models.IntegerField()
    special_defense = models.CharField(max_length=255)
    special_attack = models.CharField(max_length=255)
    defense = models.CharField(max_length=255)
    attack = models.CharField(max_length=255)
    hp = models.CharField(max_length=255)
    speed = models.CharField(max_length=255)
    evolution = models.CharField(max_length=255)

    def __str__(self):
        return self.name

