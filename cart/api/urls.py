from django.urls import path
from cart.api.views.cart import CartView, OrderListView, OrderDetailView, ManageCartAPIView

app_name = 'api'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('manage-cart/', ManageCartAPIView.as_view(), name='add_or_remove_from_cart'),
    path('order-list/', OrderListView.as_view(), name='order_list'),
    path('order-detail/<pk>/', OrderDetailView.as_view(), name='order_detail'),

]




