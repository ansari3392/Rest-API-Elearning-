from django.urls import path, include

app_name = 'account'

urlpatterns = [
    path('', include('account.api.urls'))
]
