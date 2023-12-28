

from celery import shared_task
from . import utils as ml_utils
from profiles import utils as profiles_utils
from movies.models import Movie
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
@shared_task
def train_surprise_model_task(n_epochs=20, verbose=True):
    ml_utils.train_surprise_model()


@shared_task
def batch_user_prediction_task(user_ids=None, start_page=0, offset=250, max_pages=1000):
    model = ml_utils.load_model()
    Suggestion = apps.get_model('suggestions', 'Suggestion')
    ctype = ContentType.objects.get(app_label='movies', model='movie')
    if user_ids is None:
        user_ids = profiles_utils.get_recent_users(days_ago=7, ids_only=True)
    movies_ids = Movie.objects.all().values_list('id', flat=True)
    end_page = start_page + offset
    movies_pop_ids = Movie.objects.all().popular().values_list('id', flat=True)[start_page:end_page]
    recently_suggested = Suggestion.objects.get_recently_suggested(movies_ids=movies_pop_ids, users_ids=user_ids)
    new_suggestions = []
    for movie_id in movies_pop_ids:
        users_done = recently_suggested.get(str(movie_id)) or []
        for user_id in user_ids:
            if user_id in users_done:
                print(movie_id, 'is done for user', user_id)
                continue
            pred = model.predict(uid=user_id, iid=movie_id).est
            print(user_id, movie_id, pred)
            data = {
                "user_id": user_id,
                "object_id": movie_id,
                "value": pred,
                "content_type": ctype,
            }
            new_suggestions.append(
                Suggestion(**data)
            )
    
    Suggestion.objects.bulk_create(new_suggestions, ignore_conflicts=True)
    if end_page < max_pages:
        return batch_user_prediction_task(start_page=end_page)
    

@shared_task
def batch_single_user_prediction_task(user_id=3, start_page=0, offset=250, max_pages=1000):
    return batch_user_prediction_task(user_ids=[user_id], start_page=start_page, offset=offset, max_pages=max_pages)
