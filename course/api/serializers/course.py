from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

from categories.models import Category
from cms.api.serializers.tag import TagSerializer
from cms.models import Tag
from course.api.serializers.couesrepisode import CourseEpisodeSerializer

User = get_user_model()

from course.models import Course


class CourseSerializer(ModelSerializer):
    qs = Course.objects.prefetch_related('episodes')
    tags = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    episodes = CourseEpisodeSerializer(many=True)

    def get_tags(self, obj):
        return obj.tags.values_list('name', flat=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'sku',
            'title',
            'slug',
            'description',
            'main_mage',
            'image',
            'teacher',
            'category',
            'is_free',
            'has_discount',
            'price',
            'pre_sale',
            'published_date',
            'tags',
            'episodes'
        ]
        read_only_fields = [
            'id',
            'sku',
        ]


class CreateCourseSerializer(ModelSerializer):
    teacher = serializers.SlugRelatedField(
        slug_field='first_name',
        queryset=User.objects.filter(profile__is_teacher=True)
    )
    tag_list = serializers.ListField(required=False, write_only=True)
    tags = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False

    )

    def get_tags(self, obj):
        return obj.tags.values_list('name', flat=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'sku',
            'title',
            'slug',
            'description',
            'main_mage',
            'image',
            'teacher',
            'category',
            'is_free',
            'has_discount',
            'price',
            'pre_sale',
            'published_date',
            'tags',
            'tag_list'
        ]
        read_only_fields = [
            'id',
            'sku',
        ]
