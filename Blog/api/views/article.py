from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from Blog.api.serializers.article import ArticleSerializer
from Blog.models import Article
from cms.models import Tag


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    filterset_fields = ['title', 'description']
    # lookup_field = 'sku'
    # filterset_fields =

    def get_queryset(self):
        queryset = Article.objects.all()
        # query_params = self.request.query_params
        # if query_params.get('something'):
        #     queryset = queryset.filter(is_published=True)
        return queryset

    def get_permissions(self, *args, **kwargs):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]

    def perform_create(self, serializer):
        tag_list: list = serializer.validated_data.pop('tag_list', None)
        article: Article = serializer.save(author=self.request.user)
        tags = list()
        if tag_list:
            # tags_set = set(tag_list)
            # tags = [Tag(name=tag) for tag in tags_set]
            # Tag.objects.bulk_create(tags, ignore_conflicts=True)
            # saved_tags = Tag.objects.filter(name__in=tags_set)
            # course.tags.set(saved_tags)
            for tag in tag_list:
                tag, _ = Tag.objects.get_or_create(name=tag)
                tags.append(tag)
        article.tags.set(tags)

    def perform_update(self, serializer):
        tag_list: list = serializer.validated_data.pop('tag_list', None)
        article: Article = serializer.save()
        tags = list()
        if tag_list:  # ["something"]
            for tag in tag_list:
                tag, _ = Tag.objects.get_or_create(name=tag)
                tags.append(tag)
            article.tags.set(tags)
        elif tag_list is not None:  # if not tag_list and tag_list is not None
            article.tags.clear()
