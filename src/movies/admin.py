from django.contrib import admin

# Register your models here.
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'calculate_rating_count']
    readonly_fields = ['calculate_rating_count', 'calculate_rating_avg']


admin.site.register(Movie , MovieAdmin)