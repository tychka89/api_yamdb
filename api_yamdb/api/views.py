from rest_framework import permissions, status, viewsets
from django.shortcuts import get_object_or_404

import api.permissions as ap
import api.serializers as serializers
import reviews.models as models
from rest_framework.decorators import action
from rest_framework.response import Response


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes =(ap.IsAdmin,)

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


class GenresViewSet(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenresSerializer
    permission_classes = (ap.IsAdminOrReadOnly,)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = (ap.IsAdminOrReadOnly,)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (ap.AuthorAdminModeratorOrReadOnly,)

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
    serializer_class = serializers.CommentSerializer
    permission_classes = (ap.AuthorAdminModeratorOrReadOnly,)
    
    def perform_create(self, serializer):
        review_id=get_object_or_404(
            models.Review, id=self.kwargs['review_id']
        )
        serializer.save(
            author=self.request.user,
            review_id=review_id
        )

    def get_queryset(self):
        review_id=get_object_or_404(models.Review, id=self.kwargs['review_id'])
        new_queryset = models.Comment.objects.filter(review_id=review_id)
        return new_queryset
