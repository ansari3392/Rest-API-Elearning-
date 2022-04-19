from django.urls import path, include

app_name = 'comment'

urlpatterns = [
    path('', include('comment.api.urls'))
]
