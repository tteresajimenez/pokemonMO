# Generated by Django 2.2 on 2021-09-27 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stats',
            name='id_pokemon_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemon_api.Pokemon', unique=True),
        ),
    ]
