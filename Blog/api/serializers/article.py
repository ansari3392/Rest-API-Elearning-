from django.contrib.auth import get_user_model
from rest_framework import serializers

from Blog.models.article import Article
from utils.func import PersianDateTime

User = get_user_model()

class ArticleSerializer(serializers.ModelSerializer):
    tag_list = serializers.ListField(required=False, write_only=True)
    tags = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    @staticmethod
    def get_tags(obj):
        return obj.tags.values_list('name', flat=True)

    def get_created(self, obj):
        return PersianDateTime(obj.created)

    @staticmethod
    def get_author(article):
        return article.author.first_name

    class Meta:
        model = Article
        fields = (
            'id',
            'sku',
            'title',
            'description',
            'main_image',
            'image',
            'slug',
            'author',
            'is_published',
            # 'category',
            'viewed',
            'tags',
            'tag_list',
            'created'
        )
        read_only_fields = (
            'sku',
            'slug',
            'is_published',
            'viewed',
        )




