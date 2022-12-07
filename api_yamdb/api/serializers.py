from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorieSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Categories.
    """
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Genre.
    """
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    """
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorieSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        read_only_fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating')


class TitleCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    """
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title
