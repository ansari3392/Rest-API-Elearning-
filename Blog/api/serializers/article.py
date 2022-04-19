from django.db import transaction
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from Blog.models.article import Article
from cms.api.serializers.tag import TagSerializer
from cms.models import Tag

User = get_user_model()

class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
     )

    author = serializers.SerializerMethodField()

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
        )
        read_only_fields = (
            'sku',
            'slug',
            'is_published',
            'viewed',
        )


