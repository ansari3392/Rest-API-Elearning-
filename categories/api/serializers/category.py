from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from categories.models import Category


class CategorySerializer(ModelSerializer):
    parent = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=False
    )

    class Meta:
        model = Category
        fields = [
            'sku',
            'id',
            'parent',
            'title',
            'slug',
        ]
        read_only_fields = [
            'id',
            'sku',
            'slug'
        ]

