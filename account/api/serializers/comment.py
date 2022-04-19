from rest_framework import serializers
from rest_framework.serializers import SlugRelatedField, SerializerMethodField

from comment.models import Comment
from Blog.models.article import Article


class CommentSerializer(serializers.ModelSerializer):
    article = SlugRelatedField(
        queryset=Article.objects.all(),
        slug_field='sku'
    )

    author = serializers.SerializerMethodField()

    @staticmethod
    def get_author(comment):
        return comment.author.first_name

    class Meta:
        model = Comment
        fields = [
            'sku',
            'id',
            'article',
            # 'course',
            'author',
            'description',
            'is_private',
            'is_active',
        ]
        read_only_fields = [
            'id',
            'sku',
            'is_active'
        ]


class UpdateCommentSerializer(CommentSerializer):
    article = serializers.SerializerMethodField()

    def get_article(self, obj):
        return obj.article.sku
