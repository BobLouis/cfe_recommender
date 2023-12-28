import datetime


from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import F
from django.utils import timezone

User = settings.AUTH_USER_MODEL  # 'auth.User'

class SuggestionManager(models.Manager):
    def get_recently_suggested(self, movies_ids=[], users_ids=[], days_ago=7):
        data = {}
        dalta = datetime.timedelta(days=days_ago)
        time_delta = timezone.now() - dalta
        ctype = ContentType.objects.get(app_label='movies', model='movie')
        filter_args = {
            'content_type': ctype,
            'object_id__in': movies_ids,
            'user_id__in': users_ids,
            'timestamp__lte': time_delta,
            'active': True
        }
        dataset = self.get_queryset().filter(**filter_args)
        dataset = dataset.annotate(movieId=F('object_id'), userId=F('user_id')).values("movieId", "userId")
        for d in dataset:
            print(d)
            movie_id = str(d.get('movieId'))
            user_id = d.get('userId')
            if movie_id in data:
                data[movie_id].append(user_id)
            else:
                data[movie_id] = [user_id]
        return data



class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user instance.id
    value = models.FloatField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)


    active = models.BooleanField(default=True)  # for filtering
    ## when ratings occuur after a suggestion
    rating_value = models.FloatField(null=True, blank=True)
    did_rate = models.BooleanField(default=False)
    did_rate_timestamp = models.DateTimeField(auto_now_add=False,auto_now=False, null=True, blank=True)

    objects = SuggestionManager()  # Rating.objects.get_recently_suggested()


    class Meta:
        ordering = ['-timestamp']

