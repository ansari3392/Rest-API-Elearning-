from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from comment.models.comment import Comment

from account.api.serializers.comment import CommentSerializer, UpdateCommentSerializer


class CommentView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(author=self.request.user)
        return queryset


class UpdateCommentView(UpdateAPIView):
    serializer_class = UpdateCommentSerializer
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













