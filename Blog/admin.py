from django.contrib import admin
from .models.article import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('created', )


