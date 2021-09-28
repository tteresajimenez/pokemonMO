from django.db import models


# Create your models here

class EvolutionChain(models.Model):
    """Database model for evolution chains"""
    id_evolution_chain = models.IntegerField(primary_key=True, unique=True)
    name_poke = models.CharField(max_length=255)
    def __str__(self):
        return self.name_poke

class Pokemon(models.Model):
    """Database model for pokemon information"""
    id_pokemon = models.IntegerField(primary_key=True, unique=True)
    id_evolution_fk = models.ForeignKey(EvolutionChain, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    height = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Stats(models.Model):
    """Database model for pokemon stats"""
    id_stat = models.IntegerField(primary_key=True)
    id_pokemon_fk = models.ForeignKey(Pokemon, on_delete=models.CASCADE, unique=True)
    special_defense = models.CharField(max_length=255)
    special_attack = models.CharField(max_length=255)
    defense = models.CharField(max_length=255)
    attack = models.CharField(max_length=255)
    hp = models.CharField(max_length=255)
    speed = models.CharField(max_length=255)

    def __str__(self):
        return self.defense


