from django.urls import path
from authentication.api.views.register import LoginRegisterView
from authentication.api.views.register import ValidateOTPView

app_name = 'api'

urlpatterns = [
    path('login/', LoginRegisterView.as_view(), name='login'),
    path('login/verify/', ValidateOTPView.as_view(), name='verify_login'),

]

