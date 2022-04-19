from django.urls import path, include
app_name = 'cms'

urlpatterns = [
    path('api/', include('cms.api.urls'))
]
