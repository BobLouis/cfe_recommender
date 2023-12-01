from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from ratings.models import Rating

class Movie(models.Model):
    title = models.CharField(max_length=120, unique=True)
    overview = models.TextField()
    release_date = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    ratings = GenericRelation(Rating) #queryset

    def calculate_rating_count(self):
        return self.ratings.all().count()
    
    def calculate_rating_avg(self):
        return self.ratings.all().avg()
