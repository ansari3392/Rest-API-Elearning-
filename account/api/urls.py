from django.urls import path

from account.api.views.comment import UpdateCommentView, DeleteCommentView, MyCommentView
from account.api.views.user import UserView

app_name = 'api'

urlpatterns = [
    path('', UserView.as_view(), name='my_profile'),
    path('comments/', MyCommentView.as_view(), name='my_comments'),
    path('comments/update/<pk>/', UpdateCommentView.as_view(), name='update_comment'),
    path('comments/delete/<pk>/', DeleteCommentView.as_view(), name='delete_comment'),

]

