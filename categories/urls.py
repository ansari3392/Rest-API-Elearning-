from django.urls import path, include
app_name = 'category'

urlpatterns = [
    path('', include('categories.api.urls'))
]
