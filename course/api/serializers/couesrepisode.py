from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer
from course.models import CourseEpisode, Course


class CourseEpisodeSerializer(ModelSerializer):
    course = SlugRelatedField(
        queryset=Course.objects.all(),
        slug_field='sku',
        required=False
    )
    
    class Meta:
        model = CourseEpisode
        fields = [
            # 'id',
            # 'sku',
            'course',
            'number',
            'title',
            # 'slug',
            'video',
            'video_poster',
            'duration',
            'is_free',
        ]
        read_only_fields = [
            # 'id',
            # 'sku',
        ]
