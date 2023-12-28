from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_http_methods
from .models import Rating

from ml import tasks as ml_tasks

@require_http_methods(['POST'])
def rate_movie_view(request):
    if not request.htmx:
        return HttpResponse("Not allowed", status=400)
    object_id = request.POST.get('object_id')
    rating_value = request.POST.get('rating_value')

    if object_id is None or rating_value is None:

        response = HttpResponse("skipping", status=200)
        response['HX-Trigger'] = "did-skip-movie"

        return response

    user =  request.user
    message = "You must <a href='/accounts/login/'>login</a> to rate this movie."
    if user.is_authenticated:
        message = "<span class='bg-danger text-light px-3 rounded'>error occur</span>"
        ctype = ContentType.objects.get(app_label='movies', model='movie')
        rating_obj = Rating.objects.create(content_type=ctype, object_id=object_id, value=rating_value,user=user)
        if rating_obj.content_object is not None:
            total_new_suggestion = request.session.get('total-new-suggestion') or 0
            item_rated = request.session.get('item_rated') or 0
            item_rated += 1
            request.session['item_rated'] = item_rated
            print('item_rated', item_rated)
            if item_rated % 5 == 0:
                print("trigger new suggestions")
                users_ids = [user.id]
                ml_tasks.batch_user_prediction_task.apply_async(kwargs={
                    'user_ids': users_ids,
                    'start_page': total_new_suggestion,
                    'max_pages': 10,
                    })
                #This means that the task will be sent to a Celery worker to be processed in the background, allowing the web server to continue handling other requests without waiting for this task to complete.

            message = "<span class='bg-success text-light px-3 rounded'>Rating saved !</span>"
            response = HttpResponse(message, status=200)
            response['HX-Trigger-After-Settle'] = "did-rate-movie"
            return response
    return HttpResponse(message, status=200)