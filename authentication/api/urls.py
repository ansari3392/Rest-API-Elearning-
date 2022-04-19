from django.urls import path
from authentication.api.views.register import RegisterView

app_name = 'api'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='registration'),

]

