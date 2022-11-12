from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from api.validators import year_validate
from django.core.validators import MaxValueValidator, MinValueValidator

slug_regex_validator = [RegexValidator(regex=r'^[-a-zA-Z0-9_]+$',
                                       message='Недопустимый символ в slug')]


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    CHOICES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    username = models.CharField(max_length=150, unique=True,)
    email = models.EmailField(max_length=254, unique=True,)
    role = models.CharField(max_length=150, choices=CHOICES, default=USER,)
    bio = models.TextField(verbose_name='Биография', blank=True,)
    first_name = models.CharField(max_length=150, blank=True,)
    last_name = models.CharField(max_length=150, blank=True,)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Category(models.Model):
    name = models.CharField(max_length=256,)
    slug = models.SlugField(max_length=50, unique=True,
                            validators=slug_regex_validator)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100,)
    slug = models.SlugField(unique=True,
                            validators=slug_regex_validator)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100,)
    year = models.IntegerField(validators=[year_validate])
    description = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Произведение - Жанр'
        verbose_name_plural = 'Произведение - Жанр'

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Укажите значение от 1 до 10'),
            MaxValueValidator(10, 'Укажите значение от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True,)

    class Meta:
        unique_together = ('title', 'author',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return 'Отзыв "{}" автора "{}" к произведению "{}"'.format(
            self.id, self.author, self.title)


class Comment(models.Model):
    review = models.ForeignKey(
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
            self.id, self.author, self.review)
