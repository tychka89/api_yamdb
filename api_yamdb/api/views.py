from rest_framework import viewsets
from django.shortcuts import get_object_or_404

import api.serializers as serializers
import reviews.models as models


class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        title_id=get_object_or_404(models.Title, id=self.kwargs['title_id'])
        serializer.save(
            author=self.request.user,
            title_id=title_id
        )

    def get_queryset(self):
        title_id=get_object_or_404(models.Title, id=self.kwargs['title_id'])
        new_queryset = models.Review.objects.filter(title_id=title_id)
        return new_queryset


class CommentsViewSet(viewsets.ModelViewSet):
    pass
