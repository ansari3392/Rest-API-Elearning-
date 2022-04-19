from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cms.api.views.tag import TagView

app_name = 'api'
router = DefaultRouter()
router.register('tags', TagView, basename='tag')
urlpatterns = router.urls
