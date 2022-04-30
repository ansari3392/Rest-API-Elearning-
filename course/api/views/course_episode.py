from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework import status

from course.api.serializers.couesrepisode import CourseEpisodeSerializer
from course.models import CourseEpisode


class ListEpisodeView(ListAPIView):
    serializer_class = CourseEpisodeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_sku = self.request.query_params.get('course_sku')
        if course_sku:
            queryset = CourseEpisode.objects.filter(course__sku=course_sku)
        else:
            raise ValidationError({'status': status.HTTP_400_BAD_REQUEST})
        return queryset

class CourseEpisodeView(ModelViewSet):
    serializer_class = CourseEpisodeSerializer
    queryset = CourseEpisode.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve']:
            return []
        return [IsAdminUser()]

    def list(self, request, *args, **kwargs):
        pass


