from django.contrib import admin
from pokemon_api import models

# Register your models here.
#I register the module pokemon to check it on the admin setup
admin.site.register(models.Pokemon)