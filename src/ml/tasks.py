from celery import shared_task
from . import utils as ml_utils
from profiles import utils as profiles_utils
from movies.models import Movie

@shared_task
def train_surprise_model_task(n_epochs=20, verbose=True):
    ml_utils.train_surprise_model()


@shared_task
def batch_user_prediction_task(start_page=0, offset=250, max_pages=1000):
    model = ml_utils.load_model()
    recent_user_ids = profiles_utils.get_recent_users(days_ago=7, ids_only=True)
    movies_ids = Movie.objects.all().values_list('id', flat=True)
    end_page = start_page + offset
    movies_pop_ids = Movie.objects.all().popular().values_list('id', flat=True)[start_page:end_page]

    for movie_id in movies_pop_ids:
        for user_id in recent_user_ids:
            pred = model.predict(uid=user_id, iid=movie_id).est
            print(user_id, movie_id, pred)
    if end_page < max_pages:
        return batch_user_prediction_task(start_page=end_page)
    

@shared_task
def batch_update_user_prediction_task(user_id=3, start_page=0, offset=250, max_pages=1000):
    model = ml_utils.load_model()
    recent_user_ids = [user_id]
    movies_ids = Movie.objects.all().values_list('id', flat=True)
    end_page = start_page + offset
    movies_pop_ids = Movie.objects.all().popular().values_list('id', flat=True)[start_page:end_page]
    i=0
    for movie_id in movies_ids:
        for user_id in recent_user_ids:
            pred = model.predict(uid=user_id, iid=movie_id).est
            print(user_id, movie_id, pred, i)
            i+=1
