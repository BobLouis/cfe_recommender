# Generated by Django 4.2.8 on 2023-12-18 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_movie_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
