from rest_framework import exceptions, filters, permissions, status, viewsets
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from api_yamdb.settings import DEFAULT_FROM_EMAIL
import api.permissions as ap
import api.serializers as serializers
import reviews.models as models
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from django.db.utils import IntegrityError
from django.db.models import Avg

from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from api.filters import TitlesFilter


@api_view(['POST'])
def signup(request):
    serializer = serializers.SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, create = models.User.objects.get_or_create(
            **serializer.validated_data
        )
    except IntegrityError:
        raise exceptions.ValidationError('Неверное имя пользователя или email')
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='YaMDb регистрация',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_token(request):
    serializer = serializers.TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        models.User,
        username=serializer.validated_data.get('username')
    )

    if default_token_generator.check_token(
        user, serializer.validated_data.get('confirmation_code')
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (ap.IsAdmin,)

    @action(
        methods=[
            'get',
            'patch',
        ],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=serializers.UserEditSerializer,
    )
    def users_own_profile(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (ap.IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenresSerializer
    permission_classes = (ap.IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = models.Title.objects.annotate(rating=Avg('review__score'))
    serializer_class = serializers.TitleGetSerializer
    permission_classes = (ap.IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('category', 'genre')
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.TitleGetSerializer
        return serializers.TitlePostSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (ap.AuthorAdminModeratorOrReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(models.Title, id=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            title=title
        )

    def get_queryset(self):
        title = get_object_or_404(models.Title, id=self.kwargs.get('title_id'))
        new_queryset = models.Review.objects.filter(title=title)
        return new_queryset


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (ap.AuthorAdminModeratorOrReadOnly,)

    def perform_create(self, serializer):
        review = get_object_or_404(
            models.Review, id=self.kwargs.get('review_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )

    def get_queryset(self):
        review = get_object_or_404(models.Review,
                                      id=self.kwargs.get('review_id'))
        new_queryset = models.Comment.objects.filter(review=review)
        return new_queryset
