from django.urls import path, include
from rest_framework.routers import DefaultRouter
from course.api.views.course import CourseView
from course.api.views.course_episode import CourseEpisodeView, ListEpisodeView

app_name = 'api'
urlpatterns = [
    path('episodes-list/', ListEpisodeView.as_view(), name='episodes_list'),
]

router = DefaultRouter()
router.register('courses', CourseView, basename='course')
router.register('course-episodes', CourseEpisodeView, basename='course-episode')

urlpatterns += router.urls
