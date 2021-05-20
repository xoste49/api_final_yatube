from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title',)
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate(self, data):
        """ Проверяем повторную подписку """
        if Follow.objects.filter(
                user=self.context.get('request').user,
                following=data['following']
        ):
            raise serializers.ValidationError("Вы уже подписанны")
        return data

    def validate_following(self, following):
        """ Проверяем подписку на самого себя """
        if self.context.get('request').method == 'POST':
            if self.context.get('request').user == following:
                raise serializers.ValidationError(
                    "Попытка подписаться на самого себя"
                )
        return following

    class Meta:
        fields = ('user', 'following',)
        model = Follow
