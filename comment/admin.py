from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'is_active')
    list_filter = ('created',)
    list_editable = ('is_active',)
