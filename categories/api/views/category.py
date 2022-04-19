from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from categories.api.serializers.category import CategorySerializer
from categories.models import Category


class CategoryView(ModelViewSet):
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filterset_fields = (
        'sku',
        'slug',
        'parent__sku',
        'parent__slug'
    )

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]

    def get_queryset(self):
        """
        Return Just Parent Categories In List APis.
        """
        return Category.objects.filter(parent=None) if self.action == "list" else Category.objects.all()
