# Generated by Django 4.2.7 on 2023-12-01 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_rating_avg_movie_rating_count_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['-timestamp']},
        ),
    ]