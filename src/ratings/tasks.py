import random
from django.contrib.auth import get_user_model
from movies.models import Movie 
from celery import shared_task
from .models import Rating, RatingChoice    
from django.contrib.contenttypes.models import ContentType
User = get_user_model() 


@shared_task(name='generate_fake_reviews_task')
def generate_fake_reviews(count=100,users=10, null_avg=False):
    user_s = User.objects.first()
    user_e = User.objects.last()
    random_user_ids = random.sample(range(user_s.id, user_e.id), users)
    users = User.objects.filter(id__in=random_user_ids)
    movies = Movie.objects.all().order_by("?")[:count] 
    movie_ctype = ContentType.objects.get_for_model(Movie)
    if null_avg:
        movies = Movie.objects.filter(rating_avg_isnull=True).order_by("?")[:count]

    n_rating = movies.count() 
    rating_choices = [x for x in RatingChoice.values if x != None]
    user_ratings = [random.choice(rating_choices) for _ in range(n_rating)]


    new_ratings = []
    for movie in movies:
        rating_obj = Rating.objects.create(
            content_object=movie,
            # content_type=movie_ctype,
            # object_id=movie.id,
            value=user_ratings.pop(),
            
            user=random.choice(users)
        )

        new_ratings.append(rating_obj)

    return new_ratings