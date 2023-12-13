from django.contrib import admin

# Register your models here.
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'rating_count', 'rating_avg', 'rating_last_updated']
    readonly_fields = ['calculate_rating_count',
                       'rating_avg_display', 'rating_count', 'id']
    search_fields = ['title']
    search_fields = ['id']

admin.site.register(Movie , MovieAdmin)