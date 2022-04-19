from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.api.views.user import UserView
from account.api.views.comment import CommentView, UpdateCommentView, DeleteCommentView

app_name = 'api'

urlpatterns = [
    path('', UserView.as_view(), name='my_profile'),
    path('comments/', CommentView.as_view(), name='my_comments'),
    path('comments/update/<pk>/', UpdateCommentView.as_view(), name='update_comment'),
    path('comments/delete/<pk>/', DeleteCommentView.as_view(), name='delete_comment'),

]

