from rest_framework.viewsets import ModelViewSet
from cms.api.serializers.tag import TagSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from cms.models import Tag


class TagView(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]
