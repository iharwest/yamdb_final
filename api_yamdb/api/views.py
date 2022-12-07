from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.vars import DEFAULT_EMAIL
from reviews.models import Category, Genre, Title
from user.models import User
from user.serializers import TokenSerializer, UserSerializer
from .filters import TitleFilter
from .pagination import YamPagination
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorieSerializer, GenreSerializer,
                          TitleCreateSerializer, TitleSerializer)


class CreateDestroyListViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateDestroyListViewSet):
    """
    Вьюсет для модели Categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorieSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class GenreViewSet(CreateDestroyListViewSet):
    """
    Вьюсет для модели Genre.
    """
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Title.
    """
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = YamPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    POST_PATCH_METHOD = ['create', 'update', 'partial_update']

    def get_serializer_class(self):
        if self.action in TitleViewSet.POST_PATCH_METHOD:
            return TitleCreateSerializer
        return TitleSerializer


class APISignUp(APIView):
    """Создает пользователя и посылает код подтверждения."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not User.objects.filter(username=request.data['username'],
                                   email=request.data['email']).exists():
            serializer.save()
        user = get_object_or_404(User, username=serializer.data['username'])
        code = default_token_generator.make_token(user)
        send_mail(
            subject='Confirmation code',
            message=f'Your confirmation code {code}',
            from_email=DEFAULT_EMAIL,
            recipient_list=[user.email]
        )
        return Response(
            {'email': serializer.data['email'],
             'username': serializer.data['username']},
            status=status.HTTP_200_OK)


class APIToken(APIView):
    """Посылает токен новому пользователю."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.data['username'])
        code = serializer.data['confirmation_code']

        if default_token_generator.check_token(user, code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response({'confirmation code': 'Invalid confirmation code'},
                        status=status.HTTP_400_BAD_REQUEST)
