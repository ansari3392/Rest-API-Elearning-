from django.urls import path, include
app_name = "cart"
urlpatterns = [
    path('api/', include('cart.api.urls'))

]
