from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .permissions import IsAdmin
from .serializers import AdminSerializer, UserSerializer


class AdminViewSet(ModelViewSet):
    """Возвращает пользователя по имени для пользователя с правами
    администратора, позволяет его изменять.
    Возвращает пользователю его профиль по эндпойнту 'me', позволяет
    его изменять."""
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'get':
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(
            user, data=request.data, partial=True, many=False)
        serializer.is_valid()
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
