from audioop import avg
from rest_framework import serializers
from reviews.models import User, Category, Genre, Title, Review, Comment
from rest_framework.exceptions import ValidationError
from django.db.models import Avg


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )

class UserEditSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    genre = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'category',
            'genre', 'description', 'rating'
        )
    
    def get_rating (self, obj):
        rate_title = Review.objects.filter(id=obj.id)
        num = rate_title.aggregate(Avg('score'))['score__avg']
        return num


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'title_id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = data['title_id']
        score = data['score']
        if request.method == 'POST':
            if Review.objects.filter(title_id=title_id,
                                     author=author).exists():
                raise ValidationError('На одно произведение пользователь '
                                      'может оставить только один отзыв')
            if score <= 0 or score > 10:
                raise ValidationError('Score должен быть от 1 до 10!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'review_id', 'text', 'author', 'pub_date')
