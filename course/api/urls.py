from django.urls import path, include
from rest_framework.routers import DefaultRouter
from course.api.views.course import CourseView
from course.api.views.course_episode import CourseEpisodeView

app_name = 'api'

router = DefaultRouter()
router.register('courses', CourseView, basename='course')
router.register('course-episodes', CourseEpisodeView, basename='course-episode')
urlpatterns = router.urls
