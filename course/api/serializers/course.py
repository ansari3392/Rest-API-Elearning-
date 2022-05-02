from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from categories.models import Category
from course.api.serializers.couesrepisode import CourseEpisodeSerializer
from utils.func import PersianDateTime

User = get_user_model()

from course.models import Course


class CourseSerializer(ModelSerializer):
    tags = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    episodes = CourseEpisodeSerializer(many=True)
    total_duration = SerializerMethodField()
    created = serializers.SerializerMethodField()

    def get_tags(self, obj):
        return obj.tags.values_list('name', flat=True)

    def get_total_duration(self, obj):
        duration = obj.total_duration
        return str(duration)

    def get_created(self, obj):
        return PersianDateTime(obj.created)

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
            'episodes',
            'total_duration',
            'created'
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
