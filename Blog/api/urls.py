from rest_framework.routers import DefaultRouter

from Blog.api.views import (
    ArticleViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='article')
urlpatterns = router.urls
