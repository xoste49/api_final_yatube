from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework import generics, filters

from .models import Post, Group, Comment, Follow
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, GroupSerializer, CommentSerializer, \
    FollowSerializer


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user', 'following',]
