from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from comment.api.serializers.comment import CommentSerializer
from comment.models.comment import Comment


class MyCommentView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(author=self.request.user)
        return queryset

class UpdateCommentView(UpdateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(author=self.request.user, is_active=False)
        return queryset

class DeleteCommentView(DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(author=self.request.user, is_active=False)
        return queryset













