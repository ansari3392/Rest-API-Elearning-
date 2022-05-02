from django.db.models import OuterRef, ExpressionWrapper, Sum, Subquery
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from cms.models import Tag
from course.api.serializers.course import CourseSerializer, CreateCourseSerializer
from course.models import Course


class CourseView(ModelViewSet):
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = Course.objects.all().annotate(
            total_duration=Sum('episodes__duration')
        ).prefetch_related('episodes')
        return queryset

    def get_serializer_class(self):
        return CourseSerializer if self.action in ['list', 'retrieve'] else CreateCourseSerializer

    def perform_create(self, serializer):
        tag_list: list = serializer.validated_data.pop('tag_list', None)
        course: Course = serializer.save()
        tags = list()
        if tag_list:
            # tags_set = set(tag_list)
            # tags = [Tag(name=tag) for tag in tags_set]
            # Tag.objects.bulk_create(tags, ignore_conflicts=True)
            # saved_tags = Tag.objects.filter(name__in=tags_set)
            # course.tags.set(saved_tags)
            for tag in tag_list:
                tag, _ = Tag.objects.get_or_create(name=tag)
                tags.append(tag)
        course.tags.set(tags)

    def perform_update(self, serializer):
        tag_list: list = serializer.validated_data.pop('tag_list', None)
        course: Course = serializer.save()
        tags = list()
        if tag_list:  # ["something"]
            for tag in tag_list:
                tag, _ = Tag.objects.get_or_create(name=tag)
                tags.append(tag)
            course.tags.set(tags)
        elif tag_list is not None:  # if not tag_list and tag_list is not None
            course.tags.clear()
