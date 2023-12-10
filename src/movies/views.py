from django.views import generic

from .models import Movie

class MovieListView(generic.ListView):
    template_name = 'movies/list.html'
    paginate_by = 100
    # context => object_list
    queryset = Movie.objects.order_by("-rating_avg")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(context)
        request = self.request
        user = request.user
        if user.is_authenticated:
            object_list = context['object_list']
            object_ids = [x.id for x in object_list]
            

            qs = user.rating_set.filter(active=True,object_id__in=object_ids)
            context['my_ratings'] = {f"{x.object_id}": x.value for x in qs}
        return context



movie_list_view = MovieListView.as_view()

class MovieDetailView(generic.DetailView):
    template_name = 'movies/detail.html'
    # context => object -> id
    queryset = Movie.objects.all().order_by("-rating_avg")


movie_detail_view = MovieDetailView.as_view()