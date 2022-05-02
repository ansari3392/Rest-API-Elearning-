from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError

from comment.api.serializers.comment import CommentSerializer

from comment.models.comment import Comment


class ListCommentView(ListAPIView):
    serializer_class = CommentSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['request'] = self.request
    #     return context

    def get_queryset(self):
        article_sku = self.request.query_params.get('article_sku')
        if article_sku:
            queryset = Comment.objects.filter(is_active=True, is_private=False)
            queryset = queryset.filter(article__sku=article_sku)
        else:
            raise ValidationError({'status': status.HTTP_400_BAD_REQUEST})
        return queryset


class CreateCommentView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)














