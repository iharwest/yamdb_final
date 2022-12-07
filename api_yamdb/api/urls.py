from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import CommentViewSet, ReviewViewSet
from user.views import AdminViewSet
from .views import (APISignUp, APIToken, CategoryViewSet,
                    GenreViewSet, TitleViewSet)


app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('users', AdminViewSet, basename='users')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', APISignUp.as_view(), name='signup'),
    path('auth/token/', APIToken.as_view(), name='token'),
]
