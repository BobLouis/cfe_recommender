import os
from celery import Celery   

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')


app = Celery('cfehome')


#CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.broker_url = 'redis://localhost:1234'


app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run_movie_rating_avg_every_30': {
        'task': 'task_update_movie_ratings',
        'schedule': 60*30, # 30 minutes
    },
    'run_rating_export_every_hour': {
        'task': 'export_rating_dataset',
        'schedule': 60*60,  #1 hour
    }
}