from rest_framework import viewsets

from .models import Post, Group
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    api/v1/posts/ (GET, POST):
    получаем список всех постов или создаём новый пост

    api/v1/posts/{post_id}/ (GET, PUT(PATCH), DELETE):
    получаем, редактируем или удаляем пост по id
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrReadOnly]
