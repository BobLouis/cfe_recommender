import os
import sys  


DJANGO_SETTINGS_MODULE = "cfehome.settings"
PWD = os.getenv("PWD")
PROJECT_ROOT = "/home/louis/astraZenith/backend_recommender/recommender/src"
def init():
    os.chdir(PROJECT_ROOT)
    sys.path.insert(0, PROJECT_ROOT)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    import django
    django.setup()

init()