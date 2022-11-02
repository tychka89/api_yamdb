from django.db import models
from django.contrib.auth.models import AbstractUser


CHOICES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True,)
    email = models.EmailField(unique=True,)
    first_name = models.CharField(max_length=150,)
    last_name = models.CharField(max_length=150,)
    bio = models.TextField(verbose_name='Биография', blank=True,)
    role = models.CharField(max_length=150, choices=CHOICES, default='user',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256,)
    slug = models.CharField(max_length=50,)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100,)
    slug = models.SlugField(unique=True,)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100,)
    year = models.IntegerField()
    description = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )
    category = models.OneToOneField(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )
    rating = models.IntegerField(blank=True, null=True,)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True,)

    class Meta:
        unique_together = ('title', 'author',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return 'Отзыв "{}" автора "{}" к произведению "{}"'.format(
            self.id, self.author, self.title)


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True,)

    class Meta:
        ordering = ("id",)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return 'Комментарий "{}" автора "{}" к отзыву "{}"'.format(
            self.id, self.author, self.review_id)
