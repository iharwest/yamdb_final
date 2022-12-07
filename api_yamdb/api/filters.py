import django_filters as df
from reviews.models import Title


class TitleFilter(df.FilterSet):
    name = df.CharFilter(field_name='name', lookup_expr='contains')
    genre = df.CharFilter(field_name='genre__slug')
    category = df.CharFilter(field_name='category__slug')
    year = df.NumberFilter(field_name='year', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')
