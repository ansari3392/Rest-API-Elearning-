from django.urls import path, include
app_name = 'blog'

urlpatterns = [
    path('api/', include('Blog.api.urls'))
]
