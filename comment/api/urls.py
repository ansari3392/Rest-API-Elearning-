from django.urls import path, include
from rest_framework.routers import DefaultRouter
from comment.api.views.comment import ListCommentView, CreateCommentView

app_name = 'api'

router = DefaultRouter()
urlpatterns = [
    path('', ListCommentView.as_view(), name='comment_list'),
    path('create/', CreateCommentView.as_view(), name='create_comment'),

]
urlpatterns += router.urls
