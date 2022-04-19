from django.urls import path, include
app_name = 'authentication'

urlpatterns = [
    path('', include('authentication.api.urls'))
]
