from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from ratings.models import Rating
from django.utils import timezone
import datetime


RATING_CLAC_TIME = 1 # minutes


class Movie(models.Model):
    title = models.CharField(max_length=120, unique=True)
    overview = models.TextField()
    release_date = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    ratings = GenericRelation(Rating) #queryset
    rating_last_updated = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    rating_count = models.IntegerField(blank=True,null=True)
    rating_avg = models.DecimalField(decimal_places=2,max_digits=5,blank=True,null=True)

    def __str__(self):
        if not self.release_date:
            return f"{self.title}"
        return f"{self.title} ({self.release_date.year})"


    def rating_avg_display(self):
        now = timezone.now()
        if not self.rating_last_updated:
            return self.calculate_rating()

        if self.rating_last_updated > now - datetime.timedelta(minutes=RATING_CLAC_TIME):
            return self.rating_avg
        return self.calculate_rating()    

    def calculate_rating_count(self):
        return self.ratings.all().count()
    
    def calculate_rating_avg(self):
        return self.ratings.all().avg()
    
    def calculate_rating(self, save=True):
        rating_avg = self.calculate_rating_avg()
        rating_count = self.calculate_rating_count()
        self.rating_avg = rating_avg
        self.rating_count = rating_count
        self.rating_last_updated = timezone.now()
        if save:
            self.save() 
        return self.rating_avg
    


