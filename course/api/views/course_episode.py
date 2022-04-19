from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from course.api.serializers.couesrepisode import CourseEpisodeSerializer
from course.models import CourseEpisode


class CourseEpisodeView(ModelViewSet):
    serializer_class = CourseEpisodeSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]

    def get_queryset(self):
        course_sku = self.request.query_params.get('course_sku')
        queryset = CourseEpisode.objects.all()
        if course_sku:
            queryset = queryset.filter(course__sku=course_sku)
        return queryset
