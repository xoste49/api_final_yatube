from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Группа', help_text='Группа для записи'
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )


class Group(models.Model):
    title = models.CharField(
        'Имя', max_length=200, help_text='Максимальная длина 200 символов'
    )
    slug = models.SlugField('Адрес', unique=True)
    description = models.TextField(
        'Описание', blank=True, null=True, help_text='Описание группы'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Follow(models.Model):
    """
    user — ссылка на объект пользователя, который подписывается.
    Укажите имя связи: related_name="follower"

    author — ссылка на объект пользователя, на которого подписываются,
    имя связи пусть будет related_name="following"
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"