from django.urls import path, include
app_name = 'course'

urlpatterns = [
    path('api/', include('course.api.urls'))
]
