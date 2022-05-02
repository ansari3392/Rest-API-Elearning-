from rest_framework import serializers

from Blog.models import Article
from comment.models.comment import Comment
from utils.func import PersianDateTime


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.SlugRelatedField(
        queryset=Article.objects.all(),
        slug_field='sku',
    )
    author = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    def get_created(self, obj):
        return PersianDateTime(obj.created)

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
            'created'
        ]
        read_only_fields = [
            'id',
            'sku',
            'is_active',

        ]







