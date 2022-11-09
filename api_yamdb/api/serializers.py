from rest_framework import serializers
from reviews.models import User, Category, Genre, Title, Review, Comment
from rest_framework.exceptions import ValidationError
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator

class SignUpSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(required=True,)
    
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me"- не доступно'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,)
    confirmation_code = serializers.CharField(
        max_length=150, required=True,
    )


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
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenresSerializer(many=True)
    rating = serializers.IntegerField(default=0)    

    class Meta:
        model = Title
        fields = '__all__'
    
    """def get_rating(self, obj):
        rate_title = Review.objects.filter(id=obj.id)
        num = rate_title.aggregate(Avg('score'))['score__avg']
        return num"""

class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
		queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    ) 

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(
        validators=(MinValueValidator(1),
                    MaxValueValidator(10)))

    class Meta:
        model = Review
        fields = ('id', 'title_id', 'text', 'author', 'score', 'pub_date')


    """def validate(self, data):
        request = self.context['request']
        author = request.user
        title = data['title']
        score = data['score']
        if request.method == 'POST':
            if Review.objects.filter(title=title,
                                     author=author).exists():
                raise ValidationError('На одно произведение пользователь '
                                      'может оставить только один отзыв')
            if score <= 0 or score > 10:
                raise ValidationError('Score должен быть от 1 до 10!')
        return data"""


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'review_id', 'text', 'author', 'pub_date')
