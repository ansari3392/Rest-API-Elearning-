from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from Blog.api.serializers.article import ArticleSerializer
from Blog.models import Article


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    filterset_fields = ['title', 'description']
    # lookup_field = 'sku'
    # filterset_fields =

    def get_queryset(self):
        queryset = Article.objects.all()
        # query_params = self.request.query_params
        # if query_params.get('kire_khar'):
        #     queryset = queryset.filter(is_published=True)
        return queryset

    def get_permissions(self, *args, **kwargs):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
