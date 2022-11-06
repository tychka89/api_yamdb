from rest_framework import permissions, viewsets
from django.shortcuts import get_object_or_404

import api.permissions as ap
import api.serializers as serializers
import reviews.models as models

# from api.filters import TitlesFilter
from django_filters.rest_framework import DjangoFilterBackend


class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (ap.AdminPermission,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenresSerializer
    permission_classes = (ap.AdminPermission,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = (ap.AdminPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre')


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (ap.AuthorPermission,
                          permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        title_id = get_object_or_404(models.Title, id=self.kwargs['title_id'])
        serializer.save(
            author=self.request.user,
            title_id=title_id
        )

    def get_queryset(self):
        title_id = get_object_or_404(models.Title, id=self.kwargs['title_id'])
        new_queryset = models.Review.objects.filter(title_id=title_id)
        return new_queryset


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (ap.AuthorPermission,
                          permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        review_id = get_object_or_404(
            models.Review, id=self.kwargs['review_id']
        )
        serializer.save(
            author=self.request.user,
            review_id=review_id
        )

    def get_queryset(self):
        review_id = get_object_or_404(models.Review,
                                      id=self.kwargs['review_id'])
        new_queryset = models.Comment.objects.filter(review_id=review_id)
        return new_queryset
