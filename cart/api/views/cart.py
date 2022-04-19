
from django.db.models import Sum, Prefetch, OuterRef, Subquery, ExpressionWrapper, BigIntegerField
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.api.serializers.cart import OrderListSerializer, CartSerializer, AddToCartSerializer, RemoveFromCartSerializer
from cart.models import OrderItem
from cart.models.cart import Cart
from course.models import Course


class CartView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    def get_queryset(self):
        course = Course.objects.filter(id=OuterRef('course_id')).values('price')
        orderitems_qs = OrderItem.objects.annotate(
            live_price=ExpressionWrapper(Subquery(course), output_field=BigIntegerField()))
        prefetch = Prefetch('orderitems', queryset=orderitems_qs)
        qs = Cart.objects.filter(step='initial').annotate(
            total_price=Sum('orderitems__course__price')
        ).prefetch_related(prefetch)

        return qs


class ManageCartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def add_to_cart(course: Course, cart: Cart):
        cart.orderitems.update_or_create(
            course=course,
        )

    @staticmethod
    def remove_from_cart(order_item: OrderItem):
        order_item.delete()

    def post(self, *args, **kwargs):
        serializer = AddToCartSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        course: Course = serializer.validated_data.get('course')
        cart = Cart.objects.filter(user=self.request.user, step='initial').first()
        self.add_to_cart(course, cart)

        response = {
            'message': 'Product added successfully'
        }
        return Response(
            data=response,
            status=200
        )

    def delete(self, *args, **kwargs):
        cart = Cart.objects.filter(user=self.request.user, step='initial').first()
        serializer = RemoveFromCartSerializer(data=self.request.data, cart=cart)
        serializer.is_valid(raise_exception=True)
        order_item: OrderItem = serializer.validated_data.get('order_item')
        self.remove_from_cart(order_item)

        response = {
            'message': 'order item Removed successfully'
        }
        return Response(
            data=response,
            status=200
        )


class OrderListView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = (IsAuthenticated,)

    filterset_fields = (
        'created',
        'step',
    )

    def get_queryset(self):
        course = Course.objects.filter(id=OuterRef('course_id')).values('price')
        orderitems_qs = OrderItem.objects.annotate(live_price=Subquery(course))

        prefetch = Prefetch('orderitems', queryset=orderitems_qs)
        qs = Cart.order_objects.filter(user=self.request.user).annotate(
            total_price=Sum('orderitems__course__price')
        ).prefetch_related(prefetch)
        return qs


class OrderDetailView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        course = Course.objects.filter(id=OuterRef('course_id')).values('price')
        orderitems_qs = OrderItem.objects.annotate(live_price=Subquery(course))

        prefetch = Prefetch('orderitems', queryset=orderitems_qs)
        qs = Cart.order_objects.filter(user=self.request.user).annotate(
            total_price=Sum('orderitems__course__price')
        ).prefetch_related(prefetch)
        return qs
