from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from account.api.serializers.comment import CommentSerializer
from comment.models.comment import Comment


class ListCommentView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        article_sku = self.request.query_params.get('article_sku')
        queryset = Comment.objects.filter(is_active=True, is_private=False)
        if article_sku:
            queryset = queryset.filter(article__sku=article_sku)
        return queryset


class CreateCommentView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)














